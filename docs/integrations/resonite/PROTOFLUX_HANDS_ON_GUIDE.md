# 🛠️ ProtoFlux Hands-On Guide for Beginners

**Step-by-step practical instructions to use ProtoFlux scripts in Resonite - perfect for the tutorial world!**

---

## 🎯 **Quick Start: Your First ProtoFlux Script**

### **How to Open ProtoFlux:**
```
1. Press F3 (Dev Tools)
2. Look for "ProtoFlux" tab
3. Or right-click objects → "Edit ProtoFlux"
4. Or type /openProtoFlux in chat
```

### **Create Your First Node:**
```
1. Right-click empty space in ProtoFlux editor
2. Create → Value → String Value
3. Type "Hello World!" in the box
4. Right-click the node → Add → Output → String
5. Create another node: Utility → Log Message
6. Connect String output to Log Message input
```

**You just made your first ProtoFlux script!** 🎉

---

## 🎮 **5-Minute Tutorial World Scripts**

### **1. Interactive Button**
**Make a cube change color when clicked:**

```
1. Spawn cube (B → Create → Primitive → Cube)
2. Right-click cube → Edit ProtoFlux
3. Create: [Button Events] → [On Press] → [Set Color]
4. Connect: On Press → Set Color
5. Add [Color Value] → connect to Set Color
6. Test: Click the cube!
```

### **2. Proximity Door**
**Door opens when you approach:**

```
1. Spawn two cubes (door + frame)
2. Select door → Edit ProtoFlux
3. Create: [Player Position] → [Subtract] ← [Door Position] → [Magnitude] → [< 2.0] → [Set Position]
4. Connect the chain
5. Set movement to slide door up
6. Walk near it to test!
```

### **3. Color-Changing Light**
**Rainbow light that cycles automatically:**

```
1. Spawn light (B → Create → Lights → Point Light)
2. Select light → Edit ProtoFlux
3. Create: [World Time] → [Sin] → [Map Range] → [HSV to RGB] → [Set Light Color]
4. Connect: Time → Sin → Map → HSV → Set Color
5. Watch the rainbow show!
```

---

## 🎭 **Avatar Scripts to Try**

### **4. Simple Expression Changer**
```
1. Create button or use object
2. Add ProtoFlux: [Button Press] → [Set Expression]
3. Choose expression number (0-5)
4. Test by pressing button
```

### **5. Gesture Trigger**
```
1. Create ProtoFlux on object
2. Add: [Hand Tracking] → [Pose Recognizer] → [Play Animation]
3. Set gesture (thumb up, peace sign)
4. Try the gesture!
```

---

## 🌍 **World Enhancement Scripts**

### **6. Welcome Message**
```
1. ProtoFlux on world object
2. Add: [User Joined] → [Show Notification]
3. Set welcome message
4. Test with alt account
```

### **7. Teleport Pad**
```
1. Flat platform as pad
2. Add: [Trigger Enter] → [Teleport Position]
3. Set target location
4. Step on to teleport!
```

---

## 🔧 **Debugging Tips**

### **Common Issues:**
- **Not running?** Check F3 ProtoFlux is enabled
- **Not connecting?** Verify data types match
- **Lag?** Add delays or simplify calculations
- **Use [Log Message]** to debug values

### **Testing:**
- Start with 1-2 nodes
- Test each connection
- Save frequently
- Use tutorial world for practice

---

## 📚 **Using Scripts from the Guide**

### **Implementation Steps:**
1. **Choose simple script** (button/light first)
2. **Create nodes** as shown in diagrams
3. **Connect in order** (output → input)
4. **Adjust values** for your needs
5. **Test thoroughly**

### **Tutorial World Tips:**
- Use spawn platforms for testing
- Modify existing objects with permission
- Practice in empty areas
- Learn from world examples

---

## 🚀 **Progression Path**

### **Beginner (Tutorial World):**
- Interactive buttons and lights
- Simple proximity effects
- Basic color/sound changes

### **Intermediate (Your World):**
- Doors and teleporters
- Avatar expressions
- Combined multi-object scripts

### **Advanced (Complex Worlds):**
- State machines
- MCP integration
- Collaborative systems

---

## 🎯 **Key Takeaways**

**ProtoFlux Success Formula:**
1. **Start Small** - One or two nodes at a time
2. **Test Often** - Use logs to debug
3. **Learn by Doing** - Experiment freely
4. **Study Examples** - Copy working scripts
5. **Build Gradually** - Add complexity slowly

**Remember:** Every VR creator was a beginner once. The tutorial world is your playground - experiment, break things, and learn! 🎮✨

**For detailed script examples, see the [Useful ProtoFlux Scripts Guide](./USEFUL_PROTOFLUX_SCRIPTS.md).**

**Happy ProtoFluxing!** 🤖






