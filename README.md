# Flex Test

This project tests the influence of flex hints on vertical and horizontal stems.  
Steps to produce a meaningful result:

- Build the UFO:  
`python3 build_flexy_boy.py`.   
The UFO is created in a build directory, with an adjacent GlyphOrderAndAliasDB file.

- Autohint that UFO file with whichever version of `psautohint` you’re working on
```sh
psautohint build/FlexyBoy-Regular.ufo
```

- Build the font:
```sh
makeotf -r -f build/FlexyBoy-Regular.ufo
```
- Create a PDF which contains all the flex glyphs in different sizes:  
`python3 layout_flexy_boy.py`  
The PDF file is created in the build directory.
 

---

Dependencies:  
[fontParts](https://github.com/robotools/fontParts)  
[drawBot](https://github.com/typemytype/drawbot/#install)


---

Optional: play this video  
https://youtu.be/wouKI_myXxk

