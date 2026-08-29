import Foundation
import AppKit

// Apple Mail's signature pane is an NSTextView. Put the signature in one at a
// given width and photograph it: this is the layout engine that decides
// whether the logo stays beside the text, and no browser test can reach it.
let htmlPath = CommandLine.arguments[1]
let width = CGFloat(Double(CommandLine.arguments[2])!)
let outPath = CommandLine.arguments[3]

let opts: [NSAttributedString.DocumentReadingOptionKey: Any] = [
  .documentType: NSAttributedString.DocumentType.html,
  .characterEncoding: String.Encoding.utf8.rawValue,
]
guard let a = try? NSAttributedString(url: URL(fileURLWithPath: htmlPath),
                                      options: opts, documentAttributes: nil) else {
  print("PARSE FAILED"); exit(1)
}

let tv = NSTextView(frame: NSRect(x: 0, y: 0, width: width, height: 4000))
tv.isRichText = true
tv.drawsBackground = true
tv.backgroundColor = .white
tv.textContainerInset = NSSize(width: 0, height: 0)
tv.textContainer?.lineFragmentPadding = 0
tv.textContainer?.containerSize = NSSize(width: width, height: .greatestFiniteMagnitude)
tv.textContainer?.widthTracksTextView = true
tv.textStorage?.setAttributedString(a)
tv.layoutManager?.ensureLayout(for: tv.textContainer!)
let used = tv.layoutManager!.usedRect(for: tv.textContainer!)
tv.frame = NSRect(x: 0, y: 0, width: width, height: ceil(used.height) + 4)

guard let rep = tv.bitmapImageRepForCachingDisplay(in: tv.bounds) else { exit(1) }
tv.cacheDisplay(in: tv.bounds, to: rep)
try! rep.representation(using: .png, properties: [:])!.write(to: URL(fileURLWithPath: outPath))
print(String(format: "pane %.0fpx -> laid out %.0f x %.0f", width, used.width, used.height))
