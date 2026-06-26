# 🔗 ProtoFlux: Resonite's Visual Programming System

**A comprehensive guide to ProtoFlux - Resonite's revolutionary node-based visual programming system that makes complex VR experiences accessible to everyone.**

*This guide complements the [Resonite MCP Server documentation](./RESONITE_MCP_GUIDE.md) by providing detailed technical information about ProtoFlux integration.*

---

## 📚 Quick Start

ProtoFlux is Resonite's **visual programming system** - think "Scratch for VR" but with professional capabilities. Instead of writing code, you connect visual nodes with wires to create interactive experiences.

### Why ProtoFlux Matters

**Traditional Programming:**
```csharp
// 30+ lines of complex door logic
public class DoorController : MonoBehaviour {
    public float openAngle = 90f;
    private bool isOpen = false;
    void Update() {
        if (Input.GetKeyDown(KeyCode.E)) {
            StartCoroutine(ToggleDoor());
        }
    }
    // ... 20 more lines of complex logic
}
```

**ProtoFlux Equivalent:**
```
[Key Press E] → [Toggle Bool] → [Lerp Float] → [Set Rotation]
```

**Result:** What takes 30 lines of complex code becomes 4 connected nodes.

---

## 🧩 Core Concepts

### Nodes
Visual building blocks that perform specific functions:
- **Value Nodes**: Store data (numbers, text, colors)
- **Operation Nodes**: Perform calculations and logic
- **Flow Control**: Control execution (if/then, loops)
- **I/O Nodes**: Interface with the world (buttons, triggers)

### Wires
Connections between nodes that carry data:
- **Data Wires** (blue): Pass values between nodes
- **Execution Wires** (yellow): Control when nodes run
- **Reference Wires** (purple): Point to objects

### Components
Reusable ProtoFlux programs you can save and share.

---

## 🎛️ Essential Node Categories

### Value Nodes
```protoflux
[Integer: 42]     [String: "Hello"]     [Float: 3.14]
[Bool: True]      [Color: #FF0000]      [Vector3: (1,2,3)]
```

### Math Operations
```protoflux
[Add] [Subtract] [Multiply] [Divide] [Power] [Square Root]
[Sin] [Cos] [Lerp] [Clamp] [Absolute Value]
```

### Logic Operations
```protoflux
[Equal] [Greater Than] [And] [Or] [Not]
[If True/False branches] [Switch cases]
```

### Flow Control
```protoflux
[Sequence] [Delay] [Loop] [Break] [Wait For Event]
```

### Input/Output
```protoflux
[Button Press] [Trigger Enter] [Key Press] [Log Message]
[Set Position] [Set Rotation] [Set Color] [Play Sound]
```

---

## 🔄 Common Patterns

### Basic Interactions
**Door that opens when approached:**
```
[Player Distance] → [< 2.0] → [If True] → [Set Rotation 90°]
```

**Color-changing object:**
```
[World Time] → [Sin Wave] → [Map to Color] → [Set Material]
```

**Teleport pad:**
```
[Trigger Enter] → [Get Target Pos] → [Set Player Pos] → [Play Effect]
```

### Advanced Patterns
**State machines, data processing pipelines, recursive structures**

---

## 🎮 MCP Integration

The Resonite MCP server provides comprehensive ProtoFlux control:

### Available Tools

```bash
# Execute ProtoFlux scripts with parameters
resonite_protoflux_execute(script_name, parameters)

# Analyze ProtoFlux for performance issues
resonite_protoflux_analyze_script(script_name)

# Debug ProtoFlux execution step-by-step
resonite_protoflux_debug_session(script_name, debug_mode)

# Optimize ProtoFlux for better performance
resonite_protoflux_optimize_script(script_name, optimization_level)

# Generate documentation for ProtoFlux scripts
resonite_protoflux_document_script(script_name)
```

### Example Usage

**Trigger an animation:**
```python
result = resonite_protoflux_execute("dance_sequence", {
    "speed": 1.5,
    "intensity": 0.8,
    "loop": True
})
```

**Debug complex logic:**
```python
debug_session = resonite_protoflux_debug_session("physics_sim", "step_through")
```

---

## 🔗 OSC Integration

Control ProtoFlux via external applications using OSC:

**OSC Address Format:**
```
/avatar/parameters/ProtoFlux/[script_name]/[parameter_name]
```

**Examples:**
```
/avatar/parameters/ProtoFlux/lighting/intensity 0.8
/avatar/parameters/ProtoFlux/camera/mode 1
/avatar/parameters/ProtoFlux/effect/enable 1
```

---

## 📚 Learning Resources

### Official Documentation
- [ProtoFlux Manual](https://wiki.resonite.com/ProtoFlux)
- [Node Reference](https://wiki.resonite.com/Category:ProtoFlux_Nodes)
- [ProtoFlux Tutorials](https://wiki.resonite.com/Category:ProtoFlux_Tutorials)

### Community Resources
- [Resonite Discord](https://discord.gg/resonite) - Active community support
- YouTube tutorial channels
- Community example repositories

### Learning Path
1. **Beginners**: Hello ProtoFlux, basic interactions
2. **Intermediate**: State machines, multi-user logic
3. **Advanced**: Custom components, performance optimization

---

## 🚀 ProtoFlux Advantages

### Over Traditional Coding
- **Visual**: See your logic spatially
- **Immediate**: No compile/test cycles
- **Collaborative**: Multiple users can edit simultaneously
- **Intuitive**: Lower barrier to entry

### For VR Specifically
- **Spatial Programming**: Nodes exist in 3D space
- **Gesture-Based**: VR controller interactions
- **Live Debugging**: Watch data flow through wires
- **Multi-User**: Real-time collaborative editing

---

## 🎯 Best Practices

### Organization
- Group related nodes logically
- Use clear naming conventions
- Add comments for complex logic
- Create reusable components

### Performance
- Minimize unnecessary calculations
- Use efficient data types
- Cache frequently used values
- Profile and optimize bottlenecks

### Collaboration
- Communicate changes with team members
- Test thoroughly with multiple users
- Document complex systems
- Version control your ProtoFlux components

---

## 🔍 Troubleshooting

### Common Issues
- **Nodes not connecting**: Check data type compatibility
- **Logic not executing**: Verify execution flow and triggers
- **Performance problems**: Optimize calculations and reduce complexity
- **Multi-user sync**: Use proper networking nodes and authority settings

### Debugging Techniques
- Add `Log` nodes to output values
- Use visual debuggers to inspect data flow
- Step through execution with debug tools
- Profile performance impact

---

## 🎨 Creative Applications

### Interactive Art
- Dynamic color changes based on proximity
- Sound-reactive visual effects
- Physics-based particle systems

### Game Mechanics
- Custom physics behaviors
- Procedural content generation
- Complex AI behaviors

### Social Features
- Custom gesture systems
- Interactive furniture
- Collaborative drawing tools

### Live Performances
- Real-time lighting control
- Synchronized animations
- Interactive stage elements

---

**ProtoFlux represents the future of programming in VR: visual, spatial, and collaborative.** 🚀

For more detailed tutorials and advanced techniques, visit the [official ProtoFlux documentation](https://wiki.resonite.com/ProtoFlux).

---

*See also: [Resonite Platform Comparison](./RESONITE_VS_OTHERS.md), [Beginner's Guide](./RESONITE_BEGINNERS_GUIDE.md)*






