**<p align="center"> Good Programming Practices </p>**
_________________________________
**<p align="center"> Wroclaw University of Science and Technology </p>**
**<p align="center"> Computer Science, Faculty of Electronics, 6 semester </p>**
**<p align="center"> Radoslaw Lis </p>**

# Table of Contents
- [General info](#desc)
- [Status](#stat)

 <a name="desc"></a>
# General info
Desktop, Python application with algorithm for calculating best move based on the current board setting and user letters.

Due to the lack of own server, the project was created locally as the Gerrit repository and two mirrors were created - one on GitLab (to use and practice GitLab Runner) and one on GitHab (to do the same with Jenkins). GitLab Runner runs after every change, and Jenkins runs periodically.

After each commit, the repositories on Gitlab and Github are updated using the following commands:
```
$ git fetch -p origin
$ git push --mirror
```
 <a name="stat"></a>
# Status
**master** - production,  
**develop** - works.
