# 🍞 Understanding Chunking (Tukray Karna)

**How we cut big documents into small, digestible bites for the AI.**

---

## 🔪 What is Chunking? (Chunking Kya Hai?)

Imagine you have a **big pizza** 🍕 (a long document).
You cannot eat the whole pizza in one bite. You have to cut it into **slices** (chunks) to eat it properly.

**Chunking** bilkul yehi hai:
Hum lambe documents (jaise "Society Rules") ko chote chote **paragraphs** mein divide karte hain taake AI usay aasani se parh sake aur samajh sake.

---

## 📏 The Rules of Cutting (Kaatne Ke Usool)

Hum aise hi kahin se bhi nahi kaatate. Humare paas 2 important numbers hain:

### 1. Chunk Size = 3000 Characters
Ye hamari "Slice" ka size hai.
- Har tukda taqreeban **3000 letters** (haroof) lamba hota hai.
- Ye taqreeban **1-2 pages** ke barabar hai.
- **Kyun?** Taake har tukde mein complete baat ho, adhoori nahi.

### 2. Overlap = 500 Characters
Ye thoda tricky hai, lekin bahut zaroori hai!
Jab hum ek slice kaatate hain, to hum agle slice ko **thoda peeche se** shuru karte hain.

**Analogy:**
Socho ke aap movie dekh rahe ho, aur beech mein light chali gayi. Jab light wapis aayi, to aap movie **thoda peeche se (rewind karke)** chalate ho taake **context** miss na ho.

**Without Overlap:**
1. Slice A: "...King died."
2. Slice B: "The Queen cried..."
*Connection toot gaya!*

**With Overlap:**
1. Slice A: "...King died. The Queen..."
2. Slice B: "...King died. The Queen cried..."
*Baat judi rehti hai!* ✅

---

## 🖼️ Visual Example

Imagine ye hamara document hai:
> "Swimming pool opens at 7 AM. Children under 10 are not allowed without parents. Guests fee is Rs 500."

**Without Chunking (Too Big):**
AI might get confused with too much info.

**With Chunking (Perfect):**

*Chunk 1:*
> "Swimming pool opens at 7 AM. Children under 10 are not allowed without parents..."

*Chunk 2 (Overlap ke saath):*
> "...not allowed without parents. Guests fee is Rs 500."

Dekha? "Parents" wali baat dono taraf hai, taake baat samajhne mein galti na ho!

---

## ⚙️ How Code Does It (Code Mein Kaise Hota Hai)

Hum ek tool use karte hain jiska naam hai:
`RecursiveCharacterTextSplitter`

Iska naam mushkil hai, lekin kaam simple hai:
1. Ye pehle **paragraphs** (`\n\n`) par tornay ki koshish karta hai.
2. Agar paragraph bahut bada ho, to **lines** (`\n`) par torta hai.
3. Agar line bhi badi ho, to **words** (spaces) par torta hai.

Ye koshish karta hai ke **jumla (sentence)** beech mein se na toote!

---

## 🎯 Why is Chunking Important? (Zaroori Kyun Hai?)

1.  **Behtar Search (Better Context):**
    Agar aap poochen "Pool timings?", to computer pura 50-page ka rule book nahi padhega. Wo sirf wo **chota chunk** nikalega jisme timings likhi hain.

2.  **Memory Saving:**
    AI ka dimagh (Context Window) limited hota hai. Hum usay poori kitaab nahi de sakte, sirf zaroori pages (chunks) dete hain.

3.  **Accuracy:**
    Chote text mein jawab dhoondna aasan aur accurate hota hai.

---

## 🧠 Summary

**Chunking** = **Smart Cutting** ✂️

Hum documents ko **3000 characters** ke tukdon mein kaatate hain, aur har tukde mein **500 characters** repeat karte hain (overlap), taake koi baat beech mein se na kat jaye.

Is se O.T.T.O ko sahi jawab dhoondne mein madad milti hai!
