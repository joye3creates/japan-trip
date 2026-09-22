#!/usr/bin/env python3
"""Join extracted expenses with a place registry and emit one trip.json for the app."""
import json, collections
from pathlib import Path

D = Path(__file__).resolve().parent / "data"
RATE = 0.57          # INR per JPY, user-supplied trip average

# Categories withheld from the public view. Shopping and gifts are personal
# purchases with no value to anyone reading this as a travel record, so they are
# dropped at build time rather than hidden in the page.
EXCLUDE = {"shopping", "gifts"}

# JR passes, in rupees, as recorded on the totals tab. Assumed to cover BOTH
# travellers; if it turns out to be per person, double it here and nothing else
# changes. Its cost is spread evenly across the rides it actually covered.
JR_PASS_INR = 67700

# Days on which a rail pass was active, from the Pass column of the itinerary:
# SS covers 18-23 Nov (days 3-8), HA covers 24-27 Nov (days 9-12).
PASS_DAYS = set(range(3, 13))
PASS_MODES = {"train", "shinkansen"}

# id, name, lat, lng, city, kind, confidence
# confidence: "itinerary" = named in the planning PDF, "ledger" = named in an expense
# line, "inferred" = deduced from context and needs confirming from the paper notes.
PLACES = [
 ("igi",            "Delhi Airport",            28.5562,  77.1000, "Delhi",     "transit",    "itinerary"),
 ("haneda",         "Haneda Airport",           35.5494, 139.7798, "Tokyo",     "transit",    "itinerary"),
 ("teamlab",        "teamLab Planets",          35.6494, 139.7906, "Tokyo",     "attraction", "itinerary"),
 ("shirohige",      "Shirohige Cream Puff (Totoro)",35.6598,139.6620,"Tokyo",   "food",       "ledger"),
 ("harajuku",       "Harajuku",                 35.6702, 139.7027, "Tokyo",     "shopping",   "ledger"),
 ("shinjuku",       "Shinjuku Station",         35.6896, 139.7006, "Tokyo",     "transit",    "ledger"),
 ("toyoko-shinjuku","Toyoko Inn Shinjuku",      35.6955, 139.7031, "Tokyo",     "stay",       "itinerary"),
 ("kawaguchiko",    "Kawaguchiko Station",      35.5010, 138.7573, "Mt. Fuji",  "transit",    "itinerary"),
 ("oshino",         "Oshino Hakkai",            35.4604, 138.8286, "Mt. Fuji",  "attraction", "itinerary"),
 ("ide-sake",       "Ide Sake Brewery",         35.5090, 138.7560, "Mt. Fuji",  "experience", "ledger"),
 ("hoto-fudo",      "Hoto Fudo",                35.4966, 138.7625, "Mt. Fuji",  "food",       "ledger"),
 ("honcho",         "Honcho Street",            35.4836, 138.7930, "Mt. Fuji",  "attraction", "itinerary"),
 ("lake-kawaguchi", "Lake Kawaguchi",           35.5171, 138.7519, "Mt. Fuji",  "attraction", "itinerary"),
 ("chureito",       "Chureito Pagoda",          35.4995, 138.8009, "Mt. Fuji",  "attraction", "ledger"),
 ("kyoto-stn",      "Kyoto Station",            34.9858, 135.7585, "Kyoto",     "transit",    "itinerary"),
 ("fushimi-inari",  "Fushimi Inari",            34.9671, 135.7727, "Kyoto",     "attraction", "ledger"),
 ("kodaiji",        "Kodai-ji",                 35.0000, 135.7806, "Kyoto",     "attraction", "ledger"),
 ("uji",            "Uji",                      34.8914, 135.7997, "Kyoto",     "attraction", "ledger"),
 ("byodoin",        "Byodo-in",                 34.8895, 135.8077, "Kyoto",     "attraction", "inferred"),
 ("hiroshima-stn",  "Hiroshima Station",        34.3978, 132.4757, "Hiroshima", "transit",    "ledger"),
 ("miyajima",       "Miyajima / Itsukushima",   34.2959, 132.3197, "Hiroshima", "attraction", "itinerary"),
 ("peace-park",     "Peace Memorial Park",      34.3955, 132.4536, "Hiroshima", "attraction", "itinerary"),
 ("beppu-stn",      "Beppu Station",            33.2795, 131.5011, "Beppu",     "transit",    "itinerary"),
 ("beppu-hells",    "Hells of Beppu",           33.3161, 131.4747, "Beppu",     "attraction", "ledger"),
 ("mt-aso",         "Mt. Aso",                  32.8847, 131.1040, "Beppu",     "attraction", "ledger"),
 ("katsuoji",       "Katsuo-ji (Daruma)",       34.8608, 135.4842, "Osaka",     "attraction", "ledger"),
 ("minoh",          "Minoh",                    34.8266, 135.4707, "Osaka",     "attraction", "ledger"),
 ("osaka-stn",      "Osaka Station",            34.7025, 135.4959, "Osaka",     "transit",    "itinerary"),
 ("dotonbori",      "Dotonbori",                34.6687, 135.5013, "Osaka",     "food",       "itinerary"),
 ("shinsaibashi",   "Shinsaibashi",             34.6723, 135.5010, "Osaka",     "shopping",   "ledger"),
 ("nara",           "Nara Park",                34.6851, 135.8430, "Osaka",     "attraction", "ledger"),
 ("himeji",         "Himeji Castle",            34.8394, 134.6939, "Osaka",     "attraction", "itinerary"),
 ("kanazawa-stn",   "Kanazawa Station",         36.5781, 136.6478, "Kanazawa",  "transit",    "ledger"),
 ("kenrokuen",      "Kenroku-en",               36.5620, 136.6626, "Kanazawa",  "attraction", "ledger"),
 ("omicho",         "Omicho Market",            36.5720, 136.6560, "Kanazawa",  "food",       "ledger"),
 ("kanda-house",    "Kanda House",              36.2578, 136.9063, "Kanazawa",  "attraction", "ledger"),
 ("shirakawago",    "Shirakawa-go",             36.2578, 136.9063, "Kanazawa",  "attraction", "itinerary"),
 ("matsumoto-city", "Matsumoto",                36.2384, 137.9690, "Kanazawa",  "attraction", "inferred"),
 ("kanazawa-museum","21st Century Museum",      36.5608, 136.6586, "Kanazawa",  "attraction", "ledger"),
 ("higashi-chaya",  "Higashi Chaya District",   36.5720, 136.6672, "Kanazawa",  "attraction", "inferred"),
 ("odaiba",         "Odaiba / Yurikamome",      35.6297, 139.7754, "Tokyo",     "attraction", "ledger"),
 ("kotokuin",       "Kamakura Daibutsu",        35.3167, 139.5358, "Tokyo",     "attraction", "inferred"),
 ("sensoji",        "Senso-ji, Asakusa",        35.7148, 139.7967, "Tokyo",     "attraction", "ledger"),
 ("skytree",        "Tokyo Skytree",            35.7101, 139.8107, "Tokyo",     "attraction", "ledger"),
 ("ginza",          "Ginza",                    35.6717, 139.7650, "Tokyo",     "shopping",   "itinerary"),
 ("itoya",          "Itoya",                    35.6730, 139.7669, "Tokyo",     "shopping",   "ledger"),
 ("toyoko-osaka",   "Toyoko Inn Osaka Kyobashi",34.6968, 135.5342, "Osaka",     "stay",       "booking"),
 ("chisun-nagano",  "Chisun Grand Nagano",      36.6420, 138.1880, "Nagano",    "stay",       "booking"),
 ("toyoko-fuji",    "Toyoko Inn Fuji Kawaguchiko",35.4990,138.7560,"Mt. Fuji","stay","booking"),
 ("hale-kyoto",     "HALE Kyoto Toji",          34.9839, 135.7496, "Kyoto",     "stay",       "booking"),
 ("nishitetsu-beppu","Nishitetsu Resort Inn Beppu",33.2804,131.5063,"Beppu",    "stay",       "booking"),
 ("vista-kanazawa", "Hotel Vista Kanazawa",     36.5802, 136.6433, "Kanazawa",  "stay",       "booking"),
 ("airbnb-toshima", "Airbnb, Komagome",         35.7365, 139.7470, "Tokyo",     "stay",       "booking"),
]

# From the Expedia confirmations. Only four nights of the sixteen are covered here;
# the rest were booked through Booking.com and Airbnb and are not yet documented.
# Costs are in rupees as charged, not yen.
STAYS = [
 {"place":"toyoko-shinjuku","name":"Toyoko Inn Tokyo Shinjuku Kabukicho","source":"Expedia",
  "check_in":"2025-11-16","check_out":"2025-11-17","nights":1,"inr":8898.07,"jpy":None,
  "address":"2-20-15 Kabuki-cho, Shinjuku-ku, Tokyo","status":"stayed"},
 {"place":"toyoko-fuji","name":"Toyoko Inn Fuji Kawaguchiko Ohashi","source":"Booking.com",
  "check_in":"2025-11-17","check_out":"2025-11-18","nights":1,"inr":7138.39,"jpy":None,
  "address":"401-0301 Yamanashi, Fujikawaguchiko, Funatsu 294-1","status":"stayed"},
 {"place":"hale-kyoto","name":"HALE Kyoto Toji","source":"Booking.com",
  "check_in":"2025-11-18","check_out":"2025-11-20","nights":2,"inr":17992.00,"jpy":26892,
  "address":"Minami-ku Tojihigashimonzencho 70, Kyoto","status":"stayed"},
 {"place":"nishitetsu-beppu","name":"Nishitetsu Resort Inn Beppu","source":"Booking.com",
  "check_in":"2025-11-20","check_out":"2025-11-22","nights":2,"inr":16860.00,"jpy":25200,
  "address":"Kitahama 2-10-4, Beppu","status":"stayed"},
 {"place":"toyoko-osaka","name":"Toyoko Inn Osaka Kyobashi Sakuranomiya","source":"Expedia",
  "check_in":"2025-11-22","check_out":"2025-11-24","nights":2,"inr":12569.12,"jpy":None,
  "address":"1-8-16 Nakanocho, Miyakojima, Osaka","status":"stayed"},
 {"place":"vista-kanazawa","name":"Hotel Vista Kanazawa","source":"Booking.com",
  "check_in":"2025-11-24","check_out":"2025-11-26","nights":2,"inr":11267.00,"jpy":16840,
  "address":"Hirooka 2-13-27, Kanazawa","status":"stayed"},
 {"place":"chisun-nagano","name":"Chisun Grand Nagano","source":"Expedia",
  "check_in":"2025-11-26","check_out":"2025-11-27","nights":1,"inr":5440.17,"jpy":None,
  "address":"2-17-1 Minami Chitose, Nagano","status":"not used",
  "note":"Dropped in favour of a third night in Kanazawa. That replacement night is "
         "the one accommodation record still missing."},
 {"place":"airbnb-toshima","name":"Airbnb, Komagome","source":"Airbnb",
  "check_in":"2025-11-27","check_out":"2025-11-30","nights":3,"inr":24116.59,"jpy":None,
  "address":"1-chome-35-8 Komagome, Toshima City, Tokyo","status":"stayed"},
]
STAY_BY_DAY = {}

# day_index -> ordered place ids actually visited (best reading of itinerary + ledger)
DAY_PLACES = {
 0:["igi"], 1:["haneda","teamlab","shirohige","harajuku","shinjuku","toyoko-shinjuku"],
 2:["shinjuku","kawaguchiko","lake-kawaguchi","ide-sake","hoto-fudo","oshino","honcho"],
 3:["chureito","kyoto-stn","fushimi-inari","kodaiji"],
 4:["uji","byodoin","kyoto-stn"],
 5:["hiroshima-stn","miyajima","peace-park","beppu-stn"],
 6:["beppu-stn","mt-aso"],
 7:["beppu-hells","osaka-stn","shinsaibashi","dotonbori"],
 8:["katsuoji","minoh","osaka-stn","himeji","nara"],
 9:["kanazawa-stn","omicho","kenrokuen"],
 10:["kanazawa-stn","shirakawago","kanda-house","matsumoto-city"],
 11:["kanazawa-museum","higashi-chaya","kanazawa-stn"],
 12:["odaiba","toyoko-shinjuku"] , 13:["kotokuin","ginza"],
 14:["sensoji","skytree","ginza","itoya"], 15:["haneda","igi"],
}
DAY_PLACES[12]=["odaiba"]

# backbone inter-city movement: (day, from, to, mode)
LEGS = [
 (0,"igi","haneda","flight"), (1,"haneda","teamlab","bus"),
 (1,"teamlab","shirohige","train"), (1,"shirohige","harajuku","train"),
 (1,"harajuku","shinjuku","train"), (2,"shinjuku","kawaguchiko","train"),
 (2,"kawaguchiko","oshino","bus"), (2,"oshino","honcho","cycle"),
 (3,"kawaguchiko","chureito","train"), (3,"chureito","kyoto-stn","shinkansen"),
 (3,"kyoto-stn","fushimi-inari","train"), (3,"fushimi-inari","kodaiji","bus"),
 (4,"kyoto-stn","uji","train"), (4,"uji","kyoto-stn","train"),
 (5,"kyoto-stn","hiroshima-stn","shinkansen"), (5,"hiroshima-stn","miyajima","ferry"),
 (5,"miyajima","hiroshima-stn","ferry"), (5,"hiroshima-stn","beppu-stn","train"),
 (6,"beppu-stn","mt-aso","bus"), (6,"mt-aso","beppu-stn","bus"),
 (7,"beppu-stn","beppu-hells","bus"), (7,"beppu-hells","osaka-stn","shinkansen"),
 (7,"osaka-stn","shinsaibashi","train"), (7,"shinsaibashi","dotonbori","walk"),
 (8,"osaka-stn","minoh","train"), (8,"minoh","katsuoji","bus"),
 (8,"katsuoji","himeji","shinkansen"), (8,"himeji","nara","train"),
 (8,"nara","osaka-stn","train"), (8,"osaka-stn","kanazawa-stn","train"),
 (9,"kanazawa-stn","omicho","bus"), (9,"omicho","kenrokuen","bus"),
 (10,"kanazawa-stn","shirakawago","bus"), (10,"shirakawago","matsumoto-city","train"),
 (11,"kanazawa-stn","kanazawa-museum","bus"), (11,"kanazawa-museum","higashi-chaya","walk"),
 (12,"kanazawa-stn","odaiba","shinkansen"),
 (13,"odaiba","kotokuin","train"), (13,"kotokuin","ginza","train"),
 (14,"ginza","sensoji","train"), (14,"sensoji","skytree","walk"), (14,"skytree","itoya","train"),
 (15,"haneda","igi","flight"),
]

CITY_BY_DAY = {0:"Delhi",1:"Tokyo",2:"Mt. Fuji",3:"Fuji → Kyoto",4:"Kyoto & Uji",
 5:"Hiroshima → Beppu",6:"Beppu & Mt. Aso",7:"Beppu → Osaka",8:"Osaka, Himeji, Nara",
 9:"Kanazawa",10:"Shirakawa-go",11:"Kanazawa",12:"Tokyo",13:"Tokyo & Kamakura",
 14:"Tokyo",15:"Tokyo → Delhi"}

OPEN_QUESTIONS = [
 {"day":4,"q":"Itinerary planned Arashiyama and the Sagano railway, but every expense names Uji. Which happened?"},
 {"day":10,"q":"'matsumoto trip tix' ¥8,140 is now likelier to be Matsumoto the city than the drugstore: a Nagano hotel was booked for the 26th, so Nagano prefecture was genuinely in the plan. Confirm whether you day-tripped there."},
 {"day":11,"q":"The Chisun Grand Nagano booking for the 26th went unused when you took a third Kanazawa night instead. Cancelled in time for a refund, or forfeited? It moves the trip total by ₹5,440."},
 {"day":13,"q":"'kanazawa' travel and 'buddha temple entry' on a Tokyo day — likely Kamakura via Kanazawa-hakkei. Confirm."},
 {"day":None,"q":"Thirteen of sixteen nights are still undocumented. The Expedia confirmations cover Tokyo on the 16th and Osaka on the 22nd–23rd only; Fuji, Kyoto, Beppu, Kanazawa and the last Tokyo stretch went through Booking.com and Airbnb."},
]

def main():
    rows  = json.loads((D/"raw_expenses.json").read_text())
    daysrc= json.loads((D/"days.json").read_text())
    places={p[0]:{"id":p[0],"name":p[1],"lat":p[2],"lng":p[3],"city":p[4],
                  "kind":p[5],"confidence":p[6]} for p in PLACES}

    # --- every expense gets a home on the map, so it can fly from somewhere real
    KINDMAP={'food':'food','shopping':'shopping','experiences':'attraction',
             'travel':'transit','utilities':'other','gifts':'shopping','stays':'stay'}
    seen=collections.Counter()
    for r in rows:
        dp=[places[p] for p in DAY_PLACES.get(r["day_index"],[]) if p in places]
        want=KINDMAP.get(r["category"])
        cand=[p for p in dp if p["kind"]==want] or \
             [p for p in dp if p["kind"] not in ("transit","stay")] or dp
        if cand:
            k=seen[(r["day_index"],r["category"])]; seen[(r["day_index"],r["category"])]+=1
            r["place_id"]=cand[k%len(cand)]["id"]
        else:
            r["place_id"]=None

    # --- stays become a category of their own, converted per night and flagged
    for st in STAYS:
        if st["status"]!="stayed": continue
        per=(st["jpy"]/st["nights"]) if st.get("jpy") else (st["inr"]/st["nights"]/RATE)
        start=int(st["check_in"][-2:])-15
        for n in range(st["nights"]):
            rows.append({"day_index":start+n,"date":"","category":"stays",
                "item":st["name"],"amount":round(per),"currency":"JPY",
                "converted_from_inr":not bool(st.get("jpy")),"source":st["source"],
                "payment_mode":"prepaid","paid_by":"both",
                "note":st["address"],"place_id":st["place"],"row":0})

    # --- rides the rail pass covered carry a share of the pass, not nothing
    covered=[(dd,a,b_,m) for (dd,a,b_,m) in LEGS
             if dd in PASS_DAYS and m in PASS_MODES]
    share_jpy = round(JR_PASS_INR / len(covered) / RATE) if covered else 0
    for (dd,a,b_,m) in covered:
        rows.append({"day_index":dd,"date":"","category":"travel",
            "item":f"{m} {places[a]['name']} to {places[b_]['name']}",
            "amount":share_jpy,"currency":"JPY","pass_allocated":True,
            "mode_hint":m,"payment_mode":"rail pass","paid_by":"both",
            "note":"share of the JR passes","place_id":a,"row":0})

    # --- give transport rows a mode so the icons can branch
    for r in rows:
        if r["category"]=="travel" and not r.get("mode_hint"):
            legs=[m for (dd,a,b_,m) in LEGS if dd==r["day_index"]]
            r["mode_hint"]=legs[0] if legs else "train"

    rows=[r for r in rows if r["category"] not in EXCLUDE]

    days=[]
    for d in daysrc:
        i=d["day_index"]
        rs=[r for r in rows if r["day_index"]==i]
        by=collections.Counter()
        for r in rs:
            if r["amount"]: by[r["category"]]+=r["amount"]
        days.append({
            "day_index":i,"date":d["date"],"label":CITY_BY_DAY[i],
            "currency":d["currency"],
            "places":[p for p in DAY_PLACES.get(i,[]) if p in places],
            "legs":[{"from":a,"to":b,"mode":m} for (dd,a,b,m) in LEGS if dd==i],
            "spend":dict(by),"total":sum(by.values()),
            "stay": (lambda k: {**STAYS[k], "per_night_inr": round(STAYS[k]["inr"]/STAYS[k]["nights"],2)}
                     if k is not None else None)(STAY_BY_DAY.get(i)),
            "steps":None,                      # placeholder: no health export yet
            "photos":[],                       # placeholder: no photos yet
            "note_status":"pending",           # placeholder: paper notes not transcribed
        })

    food=[r for r in rows if r["category"]=="food" and r["item"]]
    trip={
      "name":"Japan","start":"2025-11-15","end":"2025-11-30","days_count":16,
      "travellers":["Joyee","Ananya"],
      "currency":"JPY","report_currency":"INR","rate":RATE,
      "prepaid_inr":{"Flights":80000,"Accommodation":100000,"JR passes":67700,
                     "Pre-booked transport":29017},
      "placeholders":["steps","photos","paper notes"],
      "categories":["food","travel","experiences","utilities","stays"],
      "excluded_categories":sorted(EXCLUDE),
      "shown_for":"both travellers combined",
      "jr_pass":{"inr":JR_PASS_INR,"rides_covered":len(covered),
                 "per_ride_jpy":share_jpy,"assumed":"covers both travellers"},
      "stays_documented_nights":sum(x["nights"] for x in STAYS if x["status"]=="stayed"),
      "stays_documented_inr":round(sum(x["inr"] for x in STAYS if x["status"]=="stayed"),2),
      "open_questions":OPEN_QUESTIONS,
    }
    out={"trip":trip,"places":list(places.values()),"days":days,"entries":rows,"stays":STAYS,
         "legs_flat":[{"day_index":dd,"mode":m,"from":a,"to":b_} for (dd,a,b_,m) in LEGS],
         "food_items":[{"day":r["day_index"],"item":r["item"],"amount":r["amount"]} for r in food]}
    (D/"trip.json").write_text(json.dumps(out,ensure_ascii=False,separators=(",",":")))
    print(f"places        : {len(places)}")
    print(f"days          : {len(days)}")
    print(f"legs          : {sum(len(d['legs']) for d in days)}")
    print(f"entries       : {len(rows)}")
    print(f"food items    : {len(food)}")
    print(f"trip.json     : {(D/'trip.json').stat().st_size/1024:.0f} KB")
    miss=[p for d in days for p in d["places"] if p not in places]
    print(f"unknown places: {miss or 'none'}")

main()
