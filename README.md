 <a name="stat"></a>
# Status
**<p align="center"> Good Programming Practices </p>**
_________________________________
**<p align="center"> Wroclaw University of Science and Technology </p>**
**<p align="center"> Computer Science, Faculty of Electronics, 6 semester </p>**
**<p align="center"> Radoslaw Lis </p>**

# Table of Contents
- [General info](#desc)
  *  [Algorithm](#alg)
  *  [Demo](#sc)
- [Technologies](#tech)
- [Status](#stat)

 <a name="desc"></a>
# General info
Python desktop application with algorithm for calculating best move based on the current board setting and user letters.

Due to the lack of own server, the project was created locally as the Gerrit repository and two mirrors were created - one on GitLab (to use and practice GitLab Runner) and one on GitHab (to do the same with Jenkins). GitLab Runner runs after every change, and Jenkins runs periodically.

After each commit, the repositories on Gitlab and Github are updated using the following commands:
```
$ git fetch -p origin
$ git push --mirror
```
 <a name="alg"></a>
## Algorithm
The algorithm supports the two most popular of the five moves in the game of scrabble - right angle and bridge (2) and 5) from [there](http://scrabblemania.pl/oficjalne-zasady-gry-w-scrabble), section *Ruch nastêpnego gracza*). Thanks to the creation of special patterns in which you can fit properly selected words, it provides optimal, most-scored results. It uses a dictionary with Polish words (nearly 3 million words), 
but it is possible to upload another (with fewer words) for making algorithm faster.
 <a name="sc"></a>
## Demo
![Alt Text](https://s6.gifyu.com/images/gif-minuta.gif)

 <a name="tech"></a>
# Technologies
- Python 3.7,
- PyQt5.

 <a name="stat"></a>
# Status
The plans are to add additional, more complex, but less popular types of moves - adding letters to existing words, arranging several words at once. These could be done by creating new types of patterns and a little changes in algorithm engine. Feel free to pull request.

