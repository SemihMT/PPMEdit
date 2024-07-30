# PPMEdit: Pixel Editor and Metadata Tool

PPMEdit is a Python-based GUI tool developed using the Tkinter library. It serves as a pixel editor, allowing users to create and edit 32x26 pixel images, specifically designed for use with the [P4Engine](https://github.com/SemihMT/P4Engine) and the BubbleBobble game. In addition to basic pixel manipulation, PPMEdit also supports adding metadata to individual pixels, making it a versatile tool for game development and level design.

## Features

### Canvas and Pixel Editing
- **32x26 Pixel Canvas**: This is the level layout that's used in BubbleBoblle, each pixel is a tile in-game.
- **Color Selection**: Choose from a palette of colors to paint individual pixels on the canvas.
<img src="https://github.com/user-attachments/assets/276c58e6-d7e0-4e30-93c2-b30f9b9a21db" width="400">

- **Pixel Painting and Erasing**: Easily paint pixels with the selected color or erase them to revert to the blank state.
<img src="https://github.com/user-attachments/assets/1b8cb433-1149-4944-b9bd-8f924d2fe8c5" width="400">
<img src="https://github.com/user-attachments/assets/339f381e-ffd8-40a6-a9a1-9fcd2f710eef" width="400">

### Metadata Management
- **Add & Modify Metadata**: Assign metadata to each pixel. Hovering over a pixel will show a handy tooltip with any metadata that's associated with the pixel. This metadata can include information such as tile type, special properties, or other relevant data, as long as it's representable in string format.
<img src="https://github.com/user-attachments/assets/180c302a-3264-4d60-982a-7ddb6e8d5a78" width="400">

- **Metadata Storage**: Metadata is stored alongside the pixel data, ensuring that each tile's properties are preserved when saving and loading PPM files.

### File Management
- **Save PPM Files**: Save your artwork and metadata as a PPM file, compatible with the P4Engine and BubbleBobble game.
- **Load PPM Files**: Open and edit existing PPM files, allowing for iterative design and refinement of game levels.

## How to Use PPMEdit

1. **Launch PPMEdit**: Start the application to access the main editing interface.
2. **Select a Color**: Choose your desired color from the color palette.
3. **Paint Pixels**: Right-Click on the canvas grid to paint pixels with the selected color. Right-click to erase pixels.
4. **Add Metadata**: Left-click a pixel to open the metadata editor. Enter any relevant metadata as a string and confirm to save it.
5. **Save Your Work**: Use the save function to export your design and metadata to a PPM file.
6. **Load Existing Files**: Use the load function to open and edit existing PPM files.

## WIP
- **Click and Drag selections**: Repeating the same set of actions for each pixel is tedious work...

## Use Case: BubbleBobble Level Design

PPMEdit is particularly suited for designing levels in my recreation of BubbleBobble. Each pixel on the canvas represents a tile or object in the game and has the option to store metadata for extra customizability:
- **Colors**: Define the type of tile/object. You are expected to define this inside the [P4Engine](https://github.com/SemihMT/P4Engine).
- **Metadata**: Gives the engine extra information about the tile and its starting state. Mainly used to pass the direction that enemy entities face when the level starts.

## Installation and Requirements

### Prerequisites
- Python 3.11
- Tkinter (usually included with Python)

### Installation
1. Clone the repository or download the source code.
2. Run `PPMEditor.py` using Python 3 to start the application.

### Running PPMEdit
```bash
python PPMEditor.py
```
