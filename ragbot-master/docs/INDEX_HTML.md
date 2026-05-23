# index.html - Frontend Documentation

Complete guide to understanding the chat interface UI and JavaScript functionality.

---

## 📄 File Overview

**File:** `index.html`  
**Purpose:** Modern chat widget interface for O.T.T.O chatbot  
**Lines of Code:** 165  
**Technologies:** HTML5, CSS3, Vanilla JavaScript, Marked.js  

**Key Features:**
- Floating chat trigger button
- Slide-up chat widget
- Real-time messaging
- Markdown rendering
- Typing indicator
- Smooth animations

---

## 🏗️ File Structure

```
index.html
├── <head> (Lines 3-89)
│   ├── Meta tags & title
│   ├── Google Fonts import
│   ├── Marked.js library
│   └── <style> CSS (Lines 9-89)
│
├── <body> (Lines 91-165)
│   ├── Chat trigger button (Lines 93-95)
│   ├── Chat widget container (Lines 97-110)
│   │   ├── Header
│   │   ├── Messages area
│   │   ├── Typing indicator
│   │   └── Input area
│   │
│   └── <script> JavaScript (Lines 112-163)
│       ├── DOM references
│       ├── Toggle functionality
│       ├── sendMessage()
│       └── addMessage()
```

---

## 🎨 Design System (Lines 10-15)

### CSS Custom Properties

```css
:root {
    --primary: #7c3aed;    /* Deep Purple */
    --accent: #2dd4bf;     /* Teal/Neon */
    --bg-card: #111827;    /* Dark Slate */
    --text-main: #f8fafc;  /* Off-white */
}
```

**Color Palette:**
- **Primary**: Purple (#7c3aed) - Buttons, accents
- **Accent**: Teal (#2dd4bf) - Highlights, status
- **Background**: Dark slate (#111827) - Card backgrounds
- **Text**: Off-white (#f8fafc) - Main text color

**Design Philosophy:**
- Dark mode by default
- High contrast for readability
- Modern, professional look
- Glassmorphism effects

---

## 🎯 Component Breakdown

### 1. Chat Trigger Button (Lines 19-29)

```css
#chat-trigger {
    position: fixed;
    bottom: 30px;
    right: 30px;
    width: 55px;
    height: 55px;
    border-radius: 16px;
    background: var(--primary);
    box-shadow: 0 10px 20px rgba(124, 58, 237, 0.3);
    transition: 0.3s;
}
```

**Features:**
- Fixed position (bottom-right)
- Rounded corners (16px)
- Purple gradient shadow
- Hover animation (lift + scale)

**HTML (Lines 93-95):**
```html
<div id="chat-trigger">
    <svg><!-- Message icon --></svg>
</div>
```

---

### 2. Chat Widget Container (Lines 32-41)

```css
#chat-widget {
    position: fixed;
    bottom: 100px;
    right: 30px;
    width: 360px;
    height: 550px;
    background: var(--bg-card);
    border-radius: 24px;
    display: none;  /* Hidden by default */
    animation: slideUp 0.4s ease-out;
}
```

**Specifications:**
- Dimensions: 360px × 550px
- Position: Above trigger button
- Initially hidden (`display: none`)
- Slide-up animation on open
- Glassmorphism borders

**Animation (Line 43):**
```css
@keyframes slideUp {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}
```

---

### 3. Header Section (Lines 45-52)

```html
<div class="header">
    <h3>O.T.T.O</h3>
</div>
```

**Styling:**
- Centered text
- Letter spacing: 2px
- Subtle border bottom
- Semi-transparent background

---

### 4. Messages Container (Line 55)

```css
#messages {
    flex: 1;               /* Takes remaining space */
    overflow-y: auto;      /* Scrollable */
    padding: 20px;
    display: flex;
    flex-direction: column;
    gap: 16px;
}
```

**Features:**
- Flexible height
- Auto-scroll
- 16px gap between messages
- Custom scrollbar (Lines 87-88)

---

### 5. Message Bubbles (Lines 57-68)

#### User Messages (Lines 59)

```css
.user {
    align-self: flex-end;              /* Right-aligned */
    background: var(--primary);        /* Purple */
    border-bottom-right-radius: 4px;   /* Sharp corner */
}
```

#### Bot Messages (Lines 61-64)

```css
.bot {
    align-self: flex-start;            /* Left-aligned */
    background: #1f2937;               /* Dark gray */
    border-bottom-left-radius: 4px;    /* Sharp corner */
    border: 1px solid rgba(255,255,255,0.05);
}
```

**Message Styling:**
- Max width: 85% (prevents full-width)
- Rounded corners (18px)
- Padding: 12px 16px
- Line height: 1.5

**Markdown Support (Lines 67-68):**
```css
.bot strong { color: var(--accent); }  /* Bold text in teal */
.bot p { margin: 0 0 8px 0; }
```

---

### 6. Input Area (Lines 71-84)

```html
<div class="input-area">
    <input type="text" id="user-input" placeholder="Type your message...">
    <button onclick="sendMessage()">
        <svg><!-- Send icon --></svg>
    </button>
</div>
```

**Input Field:**
- Dark background (#1f2937)
- Focus effect (purple border)
- Rounded corners (12px)

**Send Button:**
- 42px × 42px
- Purple background
- Hover: scale(1.05)
- SVG send icon

---

## 💻 JavaScript Functionality (Lines 112-163)

### DOM References (Lines 113-117)

```javascript
const widget = document.getElementById('chat-widget');
const trigger = document.getElementById('chat-trigger');
const msgContainer = document.getElementById('messages');
const userInput = document.getElementById('user-input');
const typing = document.getElementById('typing-indicator');
```

---

### Toggle Chat Widget (Lines 119-123)

```javascript
trigger.onclick = () => {
    const isHidden = widget.style.display === 'none' || widget.style.display === '';
    widget.style.display = isHidden ? 'flex' : 'none';
    if (isHidden) userInput.focus();
};
```

**Logic:**
1. Check if widget is hidden
2. Toggle `display` between `none` and `flex`
3. Auto-focus input when opened

---

### Enter Key Handler (Line 125)

```javascript
userInput.addEventListener("keypress", (e) => { 
    if(e.key === "Enter") sendMessage(); 
});
```

**Effect:** Press Enter to send message (no need to click button)

---

### `sendMessage()` Function (Lines 127-148)

```javascript
async function sendMessage() {
    const text = userInput.value.trim();
    if (!text) return;  // Ignore empty messages
    
    // 1. Display user message
    addMessage(text, 'user');
    userInput.value = '';  // Clear input
    typing.style.display = 'block';  // Show "typing..."
    
    try {
        // 2. Call backend API
        const response = await fetch('http://127.0.0.1:8000/ask', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ prompt: text })
        });
        
        // 3. Parse response
        const data = await response.json();
        typing.style.display = 'none';  // Hide "typing..."
        
        // 4. Display bot response
        addMessage(data.answer, 'bot');
    } catch (err) {
        // 5. Handle errors
        typing.style.display = 'none';
        addMessage('FastAPI Server not responding.', 'bot');
    }
}
```

#### Function Flow

1. **Validation**: Check if input is not empty
2. **User Message**: Display immediately
3. **Show Indicator**: "O.T.T.O is typing..."
4. **API Call**: POST request to backend
5. **Response**: Display bot answer
6. **Error Handling**: Show error if server down

---

### `addMessage()` Function (Lines 150-162)

```javascript
function addMessage(text, role) {
    const div = document.createElement('div');
    div.className = `msg ${role}`;  // 'msg user' or 'msg bot'
    
    if (role === 'bot') {
        div.innerHTML = marked.parse(text);  // Render Markdown
    } else {
        div.innerText = text;  // Plain text for user
    }
    
    msgContainer.appendChild(div);
    msgContainer.scrollTo({ 
        top: msgContainer.scrollHeight, 
        behavior: 'smooth' 
    });
}
```

#### Function Logic

1. **Create Element**: New `<div>` for message
2. **Set Class**: `msg user` or `msg bot`
3. **Content Rendering**:
   - Bot: Parse Markdown (bold, lists, etc.)
   - User: Plain text
4. **Append**: Add to messages container
5. **Auto-scroll**: Smooth scroll to bottom

---

## 🎨 Visual Effects

### Hover Effects

```css
#chat-trigger:hover {
    transform: translateY(-5px) scale(1.05);
}

button:hover {
    background: #6d28d9;  /* Darker purple */
    transform: scale(1.05);
}
```

### Focus States

```css
input:focus {
    border-color: var(--primary);  /* Purple border */
}
```

### Scrollbar Customization (Lines 87-88)

```css
#messages::-webkit-scrollbar {
    width: 4px;
}

#messages::-webkit-scrollbar-thumb {
    background: rgba(255,255,255,0.1);
    border-radius: 10px;
}
```

---

## 📱 Responsive Design

**Fixed Dimensions:**
- Widget: 360px × 550px
- Works on screens 400px+ wide

**Improvement Suggestions:**
```css
@media (max-width: 400px) {
    #chat-widget {
        width: calc(100vw - 40px);  /* Full width minus margins */
        height: calc(100vh - 150px);
        bottom: 20px;
        right: 20px;
    }
}
```

---

## 🔧 Customization Guide

### Change Colors

```css
:root {
    --primary: #f59e0b;    /* Orange */
    --accent: #10b981;     /* Green */
    --bg-card: #1e293b;    /* Darker */
}
```

### Adjust Widget Size

```css
#chat-widget {
    width: 400px;   /* Wider */
    height: 600px;  /* Taller */
}
```

### Change Backend URL

```javascript
// Line 136
const response = await fetch('https://your-domain.com/ask', {
```

### Add Sound Effects

```javascript
function sendMessage() {
    const audio = new Audio('send.mp3');
    audio.play();
    // ... rest of code
}
```

### Add User Avatar

```javascript
function addMessage(text, role) {
    const div = document.createElement('div');
    div.className = `msg ${role}`;
    
    if (role === 'bot') {
        div.innerHTML = `
            <img src="otto-avatar.png" alt="O.T.T.O" style="width:30px">
            ${marked.parse(text)}
        `;
    }
    // ... rest
}
```

---

## 🧪 Testing the Frontend

### Local Testing

1. **Open directly:**
   ```bash
   # Windows
   start index.html
   
   # macOS
   open index.html
   ```

2. **Use local server:**
   ```bash
   python -m http.server 3000
   # Visit: http://localhost:3000/index.html
   ```

### Browser DevTools

1. Open DevTools (F12)
2. **Console**: Check for errors
3. **Network**: Monitor API calls
4. **Elements**: Inspect styling

---

## 🐛 Common Issues

### Issue: Chat widget doesn't open
**Check:**
- JavaScript errors in console
- Correct element IDs
- CSS display property

### Issue: Messages not sending
**Check:**
- Backend server running
- Correct API URL (line 136)
- CORS enabled on backend
- Network tab for failed requests

### Issue: Markdown not rendering
**Check:**
- Marked.js loaded (line 8)
- `marked.parse()` called for bot messages
- No JavaScript errors

### Issue: Scroll not working
**Check:**
- `overflow-y: auto` on `#messages`
- `scrollTo()` function called
- Container height set correctly

---

## ♿ Accessibility Improvements

**Current Limitations:**
- No keyboard navigation
- No screen reader support
- No ARIA labels

**Recommended Additions:**
```html
<input 
    type="text" 
    id="user-input"
    placeholder="Type your message..."
    aria-label="Chat message input"
    autocomplete="off"
>

<button 
    onclick="sendMessage()"
    aria-label="Send message"
>
    <svg aria-hidden="true">...</svg>
</button>

<div 
    id="messages"
    role="log"
    aria-live="polite"
    aria-relevant="additions"
>
</div>
```

---

## 🚀 Performance Optimization

### Current Performance
- ✅ No heavy frameworks
- ✅ Inline CSS (no external file)
- ✅ Minimal JavaScript
- ✅ Single external library (Marked.js)

### Possible Improvements
1. **Lazy load Marked.js**
2. **Compress SVG icons**
3. **Cache API responses**
4. **Debounce typing indicator**

---

## 📚 Libraries Used

### Marked.js (Line 8)

```html
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
```

**Purpose:** Convert Markdown to HTML  
**Usage:** `marked.parse(text)`  
**Docs:** [marked.js.org](https://marked.js.org/)

**Example:**
```javascript
marked.parse("**Bold** and *italic*")
// Returns: "<p><strong>Bold</strong> and <em>italic</em></p>"
```

---

## 🎓 Learning Resources

- [MDN Web Docs](https://developer.mozilla.org/) - HTML/CSS/JS reference
- [Fetch API Guide](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API)
- [CSS Flexbox](https://css-tricks.com/snippets/css/a-guide-to-flexbox/)
- [Async/Await](https://javascript.info/async-await)

---

**Next:** [API Reference](API_REFERENCE.md) | [Backend Documentation](MAIN_PY.md) | [Back to README](../README.md)
