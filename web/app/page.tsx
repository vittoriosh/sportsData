import fs from "node:fs";
import path from "node:path";
import Explorer from "@/components/Explorer";

export default function Page() {
  const html = fs.readFileSync(path.join(process.cwd(), "components", "body.html"), "utf8");
  return <Explorer html={html} />;
}
