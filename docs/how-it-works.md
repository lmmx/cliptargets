In the X Window System, the “clipboard” (or, more generally, any selection like PRIMARY, SECONDARY, or CLIPBOARD) can simultaneously offer the same underlying data in multiple formats (a “superposition” of possible conversions). Each potential format is identified by a unique target atom, and requestors (programs that want the clipboard content) select whichever target/format they prefer. This mechanism is spelled out in the Inter-Client Communication Conventions Manual (ICCCM). Tools such as xclip on Linux simply implement it in a convenient user-facing way.

Below is a step-by-step breakdown of how that “superposition” of multiple data formats works, why it is called “targets” in X11, and how xclip uses it:

---

## 1. Selections, Owners, and Requestors

- **Selections**. X11 allows multiple named selections, each identified by an atom (e.g., `CLIPBOARD`, `PRIMARY`, `SECONDARY`). The clipboard you interact with via xclip is typically the `CLIPBOARD` selection.  
- **Owner**. Only one application at a time “owns” a particular selection. For example, if you run xclip and copy some text or image, xclip becomes the owner of `CLIPBOARD`.  
- **Requestor**. Another application that wants to paste (retrieve) that data from the selection becomes a “requestor.” It sends a request to the owner, asking for the selection’s contents in a certain format (or “target”).

---

## 2. Multiple Formats in “Superposition”

Even though a selection is singular (e.g., “the clipboard”), it can effectively hold data in multiple formats simultaneously. This is done by letting the owner claim that it can convert that data to multiple “targets.” Each target is just an atom naming a possible data representation. Common targets include `STRING`, `COMPOUND_TEXT`, `UTF8_STRING`, `text/html`, and more.

- **TARGETS Atom**. Under the ICCCM, owners are expected to support the special target atom `TARGETS`. When a requestor asks for `TARGETS`, the owner must reply with a list of all other targets/formats it is able to provide. Essentially, `TARGETS` is how an application can discover, “What possible data formats can you convert the selection into?”  

- **Other Common Targets**. Owners may also supply targets like `STRING` (for Latin-1 text), `UTF8_STRING` (for UTF-8 text), `image/png` (for PNG images), `text/html`, or arbitrary private formats. When the requestor actually pastes, it picks one of these targets.  

In practice, this means the data is conceptually in all those formats at once—just like a quantum “superposition.” When asked for any of them, the selection owner yields that format on-demand.

---

## 3. How xclip Implements Targets

When xclip takes ownership of the clipboard selection, it stores the user’s data internally (e.g., in memory) in a few possible ways (usually raw text, possibly additional forms like HTML or image data, depending on xclip’s options). Then xclip responds to incoming paste requests from other applications:

1. **Receive Paste Request**. The requestor does a `ConvertSelection` call, specifying which target it wants (for example, `STRING`, `UTF8_STRING`, or `text/plain`).  
2. **Check the Target**. xclip looks at that requested target atom.  
3. **Convert On Demand**. xclip either has the data cached in that format or, if needed, does an on-the-fly conversion. It then places the converted data in a property on the requestor’s window.  
4. **Notify**. xclip sends a “SelectionNotify” event indicating where the data is now stored. The requestor picks it up from there.

Because of this, the same clipboard data can be “asked for” in different ways. A legacy program might request `STRING` (Latin-1 text), while a modern program might want `UTF8_STRING`. Both can succeed if xclip presents them as targets.

---

## 4. Why the ICCCM Calls Them “Targets”

Under the ICCCM (particularly Chapter 2, “Peer-to-Peer Communication by Means of Selections”), the selection mechanism is general:

1. An application (owner) “owns” a selection, holding references to the data it wants to make available.  
2. Another application (requestor) asks for the selection to be delivered in a specific “target.”  
3. The owner either provides that format in a property on the requestor’s window or refuses if it can’t convert to that target.

Each “target” is simply an atom that names a data representation. An ICCCM-compliant clipboard tool like xclip has to support at least:

- **TARGETS** (telling requestors what other targets it offers)  
- **TIMESTAMP** (allowing requestors to check ownership time)  
- **MULTIPLE** (a way to request multiple targets in one shot)  

And then it can define more (e.g., `STRING`, `UTF8_STRING`, etc.).

---

## 5. Example Flow

Using xclip as an example:

1. **xclip Copies Something**. You run `xclip -selection clipboard -in < file.txt`. xclip becomes the owner of `CLIPBOARD`.  
2. **Another App Pastes**. Suppose a text editor wants to paste from `CLIPBOARD`.  
   - It sends an X request asking for `ConvertSelection( selection=CLIPBOARD, target=STRING, property=... )`.  
   - xclip sees the request, sees target=STRING, loads that data, and puts it into the requestor’s property as Latin-1 text.  
3. **If Another Editor Wants UTF-8**. It might request `target=UTF8_STRING`. xclip notices that target, then supplies UTF-8 text. Both requests succeed from the same underlying data.

Internally, it’s stored once, but from the outside, it can appear in multiple formats. That is the essence of the “superposition.”

---

## 6. Advantages of Multiple Targets

Having more than one format is extremely useful:
- **Compatibility**. Older apps that only understand `STRING` can still paste from the clipboard. Meanwhile, modern apps can request `UTF8_STRING`.  
- **Rich Data**. If an owner can produce complex data, it can present multiple specialized targets (e.g., HTML, PNG images, etc.) so that each requestor picks whichever format it knows best.  
- **Minimal Overhead**. The actual data only needs to be truly converted/sent when a particular target is requested.

---

## 7. Summary

- The ICCCM’s selection (clipboard) architecture inherently supports providing data in multiple possible forms.  
- Each possible format is called a “target”; the selection owner advertises which targets it can supply.  
- A requestor requests a specific target, and the owner delivers that format on demand.  
- xclip implements this faithfully: it becomes the selection owner, stores your data internally, and offers a set of targets so that any requestor can choose the format it needs.

Hence, in X11, “clipboards” do not literally store multiple versions of the data at once on the server side; rather, they store it in the owner application (like xclip). The server just knows the selection name and a set of “targets” that describe how that data can be provided. It is precisely these “targets” that give the appearance of a single clipboard holding multiple formats in “superposition.”  

This design—codified in the ICCCM—is what makes it possible for you to copy something in xclip and paste it in different programs, each retrieving the same selection but in its desired data format.
