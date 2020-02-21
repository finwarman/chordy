# chordy
A command-line guitar chord finder, written in Python  
[chordy.finwarman.com](https://chordy.finwarman.com/)

### Installation
To call _Chordy_ from anywhere, add an alias to your **~/.bash_profile**:
`echo "alias chordy='python3 /[YOUR PATH TO]/chordy/chordy.py" >> ~/.bash_profile; source ~/.bash_profile'`

### Usage

* Getting Started:
  `$ ./chordy.py`
  ```
  Available keys:

  C  C#  D  Eb  E  F  F#  G  Ab  A  Bb  B  

  Available suffixes:

  major   minor   dim     dim7    sus2    sus4    
  7sus4   7sg     alt     aug     6       69      
  7       7b5     aug7    9       9b5     aug9    
  7b9     7#9     11      9#11    13      maj7    
  maj7b5  maj7#5  maj9    maj11   maj13   m6      
  m69     m7      m7b5    m9      m11     mmaj7   
  mmaj7b5 mmaj9   mmaj11  add9    madd9   /E      
  /F      /F#     /G      /G#     /A      /Bb     
  /B      /C      /C#     m/B     m/C     m/C#    
  /D      m/D     /D#     m/D#    m/E     m/F     
  m/F#    m/G     m/G#   
  ```
* Arguments:
  * _No Args_               - List all possible keys & suffixes
  * `{key{suffix}}` (Positional Arg)     - Specify the chord to show voicing(s) for, e.g. `C#sus4`, `F`, `G/B`
  * `[-h | --help]`         - Display help text
  * `[-a | --all-voicings]` - Display all available chord voicings/positions
  
### Examples
  * `$ chordy C#sus4` - Show the first position for _C#sus4_
  * `$ chordy F -a` - Show all positions for _F major_
 
<p align="center">
  <img width="300" src="https://user-images.githubusercontent.com/1339254/74889703-bd484600-5379-11ea-90dd-e6e62e801ecf.png">
</p>
<p align="center">
  <img width="300" src="https://user-images.githubusercontent.com/1339254/74889723-cdf8bc00-5379-11ea-923b-9a206942ba6c.png">
</p>
