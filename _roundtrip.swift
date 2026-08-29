import Foundation
import AppKit

// Apple Mail's signature editor is Cocoa rich text, not a live WebView. Pasting
// runs the HTML through NSAttributedString and writing it back out runs it
// through again. This does exactly that round trip so we can see what survives.
let path = CommandLine.arguments[1]
let data = FileManager.default.contents(atPath: path)!
let opts: [NSAttributedString.DocumentReadingOptionKey: Any] = [
  .documentType: NSAttributedString.DocumentType.html,
  .characterEncoding: String.Encoding.utf8.rawValue,
]
guard let a = try? NSAttributedString(data: data, options: opts, documentAttributes: nil) else {
  print("PARSE FAILED"); exit(1)
}
let out = try! a.data(from: NSRange(location: 0, length: a.length),
  documentAttributes: [.documentType: NSAttributedString.DocumentType.html])
FileManager.default.createFile(atPath: CommandLine.arguments[2], contents: out)
print("round trip ok, \(data.count) bytes in, \(out.count) bytes out")
