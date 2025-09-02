# Changelog

All notable changes to Time Loop Runner will be documented in this file.

## [1.0.0] - 2024-12-19

### Added
- Initial release of Time Loop Runner
- Core time-rewind mechanic on collision
- Endless runner gameplay with procedural obstacles
- Physics-based ball character with jumping
- Progressive difficulty scaling
- Visual rewind indicator
- Distance-based scoring system
- Keyboard controls (SPACE to jump, ESC to quit)

### Features
- **Time Rewind System**: 3-second state history with smooth rewind animation
- **Procedural Generation**: Random obstacle spawning with two types (ground and floating)
- **Physics Engine**: Gravity-based movement with ground collision
- **UI Elements**: Score display, instructions, and rewind feedback
- **Performance**: 60 FPS gameplay with efficient state management

### Technical
- Built with pygame 2.5.2
- Deque-based state storage for memory efficiency
- Rectangle-based collision detection
- Modular class structure for easy expansion