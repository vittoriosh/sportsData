"use client";
import { useEffect } from "react";

function load(src: string) {
  return new Promise<void>((resolve, reject) => {
    const s = document.createElement("script");
    s.src = src;
    s.onload = () => resolve();
    s.onerror = () => reject(new Error("failed to load " + src));
    document.body.appendChild(s);
  });
}

// Markup is rendered server-side; the explorer script (public/app.js) then wires it up
// once the dataset (public/data.js) has loaded.
export default function Explorer({ html }: { html: string }) {
  useEffect(() => {
    const w = window as unknown as { __plLoaded?: boolean };
    if (w.__plLoaded) return;
    w.__plLoaded = true;
    load("/data.js").then(() => load("/app.js")).catch(console.error);
  }, []);
  return <div dangerouslySetInnerHTML={{ __html: html }} suppressHydrationWarning />;
}
