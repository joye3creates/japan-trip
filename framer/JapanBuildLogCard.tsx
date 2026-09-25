import { useEffect, useRef, useState } from "react"
import { addPropertyControls, ControlType } from "framer"

/**
 * Japan build log card.
 *
 * Drop it in the Playground. The video is the hook, the chip carries the day
 * count, and the day count can keep itself current by reading status.json off
 * the Netlify site instead of being edited by hand.
 *
 * @framerSupportedLayoutWidth any
 * @framerSupportedLayoutHeight auto
 */
export default function JapanBuildLogCard(props) {
    const {
        videoSrc, posterSrc, href, statusUrl,
        day, totalDays, separator,
        tagText, headline, body, figures, ctaText,
        paper, ink, inkSoft, vermillion, grain, style,
    } = props

    const [liveDay, setLiveDay] = useState<number | null>(null)
    const [still, setStill] = useState(false)
    const vid = useRef<HTMLVideoElement>(null)

    // Honour reduced motion: hold the poster, never autoplay.
    useEffect(() => {
        const mq = window.matchMedia("(prefers-reduced-motion: reduce)")
        const set = () => setStill(mq.matches)
        set()
        mq.addEventListener?.("change", set)
        return () => mq.removeEventListener?.("change", set)
    }, [])

    // status.json publishes { day, total }. If it cannot be read the hand-set
    // day stays, so a failed fetch degrades to a stale number, never a blank.
    useEffect(() => {
        if (!statusUrl) return
        let alive = true
        fetch(statusUrl, { cache: "no-store" })
            .then((r) => (r.ok ? r.json() : null))
            .then((d) => {
                if (alive && d && Number.isFinite(d.day)) setLiveDay(d.day)
            })
            .catch(() => {})
        return () => { alive = false }
    }, [statusUrl])

    const shownDay = liveDay ?? day
    const feather =
        "linear-gradient(to right,transparent 0,#000 4%,#000 96%,transparent 100%)," +
        "linear-gradient(to bottom,transparent 0,#000 5%,#000 95%,transparent 100%)"

    const noise =
        "url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E" +
        "%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='3'/%3E" +
        "%3CfeColorMatrix type='saturate' values='0'/%3E%3C/filter%3E" +
        "%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E\")"

    return (
        <div style={{ ...style, background: paper, position: "relative", overflow: "hidden" }}>
            <style>{`
              @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;800&display=swap');
              .jbl{display:grid;grid-template-columns:1.05fr 1fr;gap:38px;align-items:center;
                   padding:40px 48px;position:relative;z-index:3;
                   font-family:"Plus Jakarta Sans",system-ui,sans-serif}
              .jbl h2{font-weight:800;font-size:34px;line-height:1.2;
                      letter-spacing:-.015em;margin:18px 0 15px}
              .jbl p{margin:0}
              .jbl .body{font-size:15px;line-height:1.6;margin-bottom:20px;max-width:44ch}
              .jbl .figs{font-size:15px;font-weight:600;line-height:1.5;margin-bottom:22px}
              .jbl .chip{display:inline-flex;align-items:center;gap:9px;border-radius:999px;
                         padding:8px 16px;font-size:15px;font-weight:500;border:1px solid currentColor}
              .jbl .dot{width:6px;height:6px;border-radius:50%;flex:none}
              .jbl .cta{display:inline-flex;align-items:center;gap:8px;font-size:15px;
                        font-weight:600;padding:13px 20px;border-radius:4px;text-decoration:none}
              .jbl .media{position:relative;margin:0}
              .jbl .media video,.jbl .media img{width:100%;display:block;
                -webkit-mask-image:${feather};mask-image:${feather};
                -webkit-mask-composite:source-in;mask-composite:intersect}
              @media (max-width:860px){
                .jbl{grid-template-columns:1fr;gap:22px;padding:28px 22px}
                .jbl h2{font-size:27px}
              }
            `}</style>

            <div aria-hidden style={{
                position: "absolute", inset: 0, zIndex: 2, pointerEvents: "none",
                backgroundImage: noise, mixBlendMode: "multiply", opacity: grain,
            }} />

            <div className="jbl">
                <figure className="media">
                    {still || !videoSrc ? (
                        <img src={posterSrc} alt="" />
                    ) : (
                        <video
                            ref={vid}
                            src={videoSrc}
                            poster={posterSrc}
                            autoPlay muted loop playsInline
                            preload="metadata"
                            aria-label="A map of Japan breaking apart, every mark flying to the hour it happened"
                        />
                    )}
                </figure>

                <div>
                    <span className="chip" style={{ color: vermillion }}>
                        {tagText}
                        {separator === "dot"
                            ? <span className="dot" style={{ background: vermillion }} />
                            : <span style={{ opacity: .55 }}>&ndash;</span>}
                        Day {shownDay}/{totalDays}
                    </span>
                    <h2 style={{ color: ink }}>{headline}</h2>
                    <p className="body" style={{ color: inkSoft }}>{body}</p>
                    <p className="figs" style={{ color: ink }}>{figures}</p>
                    <a className="cta" href={href} style={{ background: ink, color: paper }}>
                        {ctaText} &#8599;
                    </a>
                </div>
            </div>
        </div>
    )
}

JapanBuildLogCard.defaultProps = {
    day: 4,
    totalDays: 16,
    separator: "dot",
    tagText: "Building with Claude Code",
    headline: "I couldn't explain the trip. So I visualized it.",
    body: "I came back from 16 days in Japan with a detailed spreadsheet, a stack of booking PDFs and over 1,000 photos, and still no good answer when friends asked how it was, or what it cost. So I'm giving myself 16 days to build one: every meal, fare, ticket and night on a single 24-hour clock, readable at a glance and worth opening up.",
    figures: "158 expense lines · 53 places · 43 journeys → one screen",
    ctaText: "See today's progress",
    paper: "#E8DCC0",
    ink: "#3B2F23",
    inkSoft: "#5C4E3C",
    vermillion: "#A83A2B",
    grain: 0.3,
    statusUrl: "https://japantripon24hrclock.netlify.app/status.json",
    href: "https://japantripon24hrclock.netlify.app/",
}

addPropertyControls(JapanBuildLogCard, {
    videoSrc:   { type: ControlType.File, title: "Loop", allowedFileTypes: ["mp4", "webm"] },
    posterSrc:  { type: ControlType.Image, title: "Poster" },
    href:       { type: ControlType.Link, title: "Link" },
    statusUrl:  { type: ControlType.String, title: "Status URL", placeholder: "https://…/status.json" },
    day:        { type: ControlType.Number, title: "Day", min: 1, max: 99, step: 1, displayStepper: true },
    totalDays:  { type: ControlType.Number, title: "Of", min: 1, max: 99, step: 1, displayStepper: true },
    separator:  { type: ControlType.Enum, title: "Separator", options: ["dot", "dash"], optionTitles: ["Dot", "Dash"], displaySegmentedControl: true },
    tagText:    { type: ControlType.String, title: "Tag" },
    headline:   { type: ControlType.String, title: "Headline", displayTextArea: true },
    body:       { type: ControlType.String, title: "Body", displayTextArea: true },
    figures:    { type: ControlType.String, title: "Figures" },
    ctaText:    { type: ControlType.String, title: "Button" },
    paper:      { type: ControlType.Color, title: "Paper" },
    ink:        { type: ControlType.Color, title: "Ink" },
    inkSoft:    { type: ControlType.Color, title: "Ink soft" },
    vermillion: { type: ControlType.Color, title: "Accent" },
    grain:      { type: ControlType.Number, title: "Grain", min: 0, max: 1, step: 0.05 },
})
