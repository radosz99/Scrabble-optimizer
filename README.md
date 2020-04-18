 <a name="stat"></a>
**<p align="center"> Good Programming Practices </p>**
_________________________________
**<p align="center"> Wroclaw University of Science and Technology </p>**
**<p align="center"> Computer Science, Faculty of Electronics, 6 semester </p>**
**<p align="center"> Radoslaw Lis </p>**

# Table of Contents
- [General info](#desc)
- [Technologies](#tech)
- [Demo](#sc)
- [Algorithm](#alg)
  *  [Patterns](#pat)
     *  [Right angle](#ang)
     *  [Bridges](#brid)
  *  [Word searching](#word)
     *  [Anagrams](#anag)
     *  [Probably valid words](#prob)
     *  [Valid words](#val)
  *  [Final result](#fin)
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

<a name="tech"></a>
# Technologies
- Python 3.7,
- PyQt5.


 <a name="sc"></a>
# Demo
[Full video on YouTube](https://www.youtube.com/watch?v=Mp1yMPCs-0Y&t=2s)
![Alt Text](https://s6.gifyu.com/images/gif-minuta.gif)
 <a name="alg"></a>
# Algorithm
The algorithm supports the two most popular of the five moves in the game of scrabble - right angle and bridge (*2)* and *5)* from [there](http://scrabblemania.pl/oficjalne-zasady-gry-w-scrabble), section *Ruch nastepnego gracza*). Thanks to the creation of special patterns in which you can fit properly selected words, it provides optimal, most-scored results. It uses a dictionary with Polish words (nearly 3 million words), 
but it is possible to upload another (with fewer words) for making algorithm faster.

 <a name="pat"></a>
 ## Patterns (*create_patterns*)
 Suppose that board looks like below (*.../optimizer/resources/board2.csv*) and letters that the user currently has are:
  ```
  g k ê p u Ÿ i
  ```
  
<p align="center">
  <img src="https://i.imgur.com/oaS7aYn.png" width=40% alt="Img"/>
</p>

According to the official rules of the game, words can be put in the vertical (down) or horizontal (right) direction, which after reverse-transposition of the board (90* counterclockwise, first row is now the previous last column) comes down to treating words that might be put in vertical direction (down) in the same way as words that might be put in horizontal direction (right). This allows to create the patterns for each of the directions by using the same method, remembering only to change the coordinates at the end (*x=y* and *y=14-x*).  

<a name="ang"></a>
### Right angles (*make_patterns*)
At the beginning, appropriate patterns are created, generally representing the word, which can be put on the board. First, the simplest patterns (so-called **right angles**) are created, which contain only one letter from the board. Their structures look like this:
  ```
  ('¿', 1, 9, 6, 2, 'h')
  ```
First element is the letter, second and third are coordinates x and y respectively, fourth and fifth are the number of free fields on the left and right respectively. The last one is direction in which word can be put (*h* - horizontal, *v* - vertical). Creating patterns involves checking each letter of empty fields on the left and on the right. If it has at least one available field on any side, it is saved - with the other needed elements - in the pattern. 

After scanning the board, the following patterns of right angle type were created: 
 ```
('¿', 1, 9, 6, 2, 'h'), ('¿', 2, 2, 2, 5, 'h'), ('u', 2, 9, 5, 1, 'h'), ('d', 2, 12, 1, 2, 'h'), 
('a', 3, 2, 2, 5, 'h'), ('i', 3, 12, 0, 2, 'h'), ('n', 5, 12, 0, 2, 'h'), ('a', 8, 5, 5, 0, 'h'), 
('a', 8, 10, 0, 1, 'h'), ('æ', 9, 5, 5, 4, 'h'), ('Ÿ', 7, 14, 7, 7, 'v'), ('e', 7, 13, 0, 7, 'v'), 
('k', 4, 8, 0, 1, 'v'), ('h', 7, 8, 1, 7, 'v'), ('t', 7, 7, 1, 7, 'v'), ('a', 5, 6, 5, 0, 'v'), 
('ê', 5, 4, 5, 0, 'v')
```

<a name="brid"></a>
### Bridges (*make_brigdes*)
Creating bridges involves searching through previously created patterns and checking if there are any that are in the same column (vertical direction) or in the same row (horizontal direction). If so, it is checked if they can be connect - sufficient number of free fields and not too large distance separating them. Their structures look like this:
  ```
('kh', 4, 8, 0, 5, 'v', 3)
  ```
At the beginning there are letters representing the bridge, then the coordinates of the letter which is more left in the case of horizontal direction or more down in the case of vertical direction. Then we have empty fields on the left and on the right (or top and bottom in the case of vertical direction), next we have direction and difference in letter coordinates. The difference here is the specific number of empty fields, which is calculated on the basis of the empty fields of both right angle patterns and the difference between their coordinates.

After scanning, the list of bridges is as follows:
  ```
('kh', 4, 8, 0, 5, 'v', 3), ('ud', 2, 9, 5, 0, 'h', 3), ('ud', 2, 9, 1, 2, 'h', 3), ('ud', 2, 9, 4, 1, 'h', 3),
('¿u', 2, 2, 0, 1, 'h', 7), ('ud', 2, 9, 3, 2, 'h', 3), ('¿u', 2, 2, 1, 0, 'h', 7), ('ud', 2, 9, 0, 2, 'h', 3),
('ud', 2, 9, 2, 2, 'h', 3) 
```
<a name="word"></a>
## Words searching (*get_valid_words*)
Word search is divided into three stages, in which more and more accurate selection is made, to finally get a list of words that can be put on the board.

<a name="anag"></a>
### Anagrams (*find_anagrams*)
From the user letters and properly converted letters contained in the patterns (i.e. from the board) one string is created, which is the basis for searching for words (anagrams), which will then be selected.  

In this case the string of letters is as follows:
```
g k ê p u Ÿ i | i u Ÿ k e ¿ h ê a d t æ n
```
The words from the dictionary are stored in a special structure of data (*trie*), thanks to which the search for anagrams takes place in a relatively short time. For this set of letters program returned 1677 anagrams:
```
['ad', 'adenkê', 'adenki', [...], 'gand¿ê', 'ganek', 'gani', [...], 'napitku', 'nat', 'natek', [...], 'pienika', 'pieniku', 'pieniu',  [...], '¿upniku', '¿uta', '¿ute']
```
<a name="prob"></a>
### Probably valid words (*find_probably_valid_words*)
At this stage, the anagrams undergo appropriate selection to get rid of words that definitely can't be put on the board. The whole process is complex - including checking whether the word contains at least one letter from the board, checking whether the word contains at least one user letter and checking whether the word contains more than two letters (maximum number of letters in the bridge), which do not belong to the user's letters (if so, the word does not meet the requirements).  

After all anagrams have gone through this process, the program now contains 249 possible words (sorted by the shortest):
```
['ag', 'au', 'gê', 'gu', 'hê', 'hi', 'hu', 'id', 'ii', 'in', 'i¿', 'ka', 'ki', 'ku', 'ni', 'nu', 'pa', 'pe', 'pi', 'tê', 'tu', 'ud', 'ut', 'uu', 'agê', 'agi', 'dêg', 'dip', 'dug', 'dup', 'gai', 'gap', 'ghi', 'gid', 'gie', 'gik', 'gin', 'git', 'gnê', 'gnu', 'g¿ê', 'hip', 'huk', 'idê', 'idu', 'idŸ', 'ikt', 'ink', 'kap', 'kaŸ', 'keg', 'kei', 'kêp', 'kia', 'kiæ', 'kie', 'kiê', 'kii', 'kin', 'kip', 'kit', 'kiŸ', 'kpa', 'kpi', 'kuæ', 'kuk', 'kun', 'kup', 'nip', 'pai', 'pak', 'paŸ', 'pêd', 'pêk', 'pêt', 'phi', 'phu', 'pia', 'piæ', 'pie', 'pik', 'pin', 'pit', 'piu', 'pnê', 'pni', 'pud', 'puh', 'puk', 'pun', 'têp', 'tik', 'tiu', 'tui', 'tuk', 'tup', 'utê', 'uti', 'Ÿga', '¿uk', '¿up', 'agiu', 'aigu', 'akiê', 'dêgi', 'dipu', 'diuk', 'dugê', 'dugi', 'dupê', 'ekip', 'epik', 'gaik', 'gapê', 'gapi', 'giêæ', 'giki', 'giku', 'ginê', 'ginu', 'guni', 'huki', 'iktu', 'inkê', 'inku', 'kagu', 'kapê', 'kapu', 'kegê', 'kegi', 'kegu', 'kepi', 'kêpa', 'kêpê', 'kiep', 'kinê', 'king', 'kinu', 'kipa', 'kipê', 'kipi', 'kipu', 'kitê', 'kitu', 'kpiæ', 'kpie', 'kpiê', 'kpin', 'kuki', 'kunê', 'kuni', 'kupa', 'kupê', 'kupi', 'kupn', 'ngui', 'nipê', 'pakê', 'paki', 'paku', 'pêdu', 'pêdŸ', 'pêka', 'pêki', 'pêku', 'pêtu', 'pieg', 'piêæ', 'piêt', 'pika', 'pikê', 'piki', 'piku', 'pink', 'pinu', 'pitê', 'pniu', 'puhê', 'puka', 'pukê', 'puki', 'puku', 'punê', 'punk', 'têgi', 'têpi', 'tikê', 'tiku', 'tukê', 'tuki', 'tupi', 'ugnê', 'ukap', 'uniê', 'unik', 'upêd', 'upiæ', 'upnê', 'Ÿgnê', '¿uki', '¿upê', 'dupkê', 'dupki', 'ekipê', 'epikê', 'epiku', 'gaiku', 'gapiê', 'gapiu', 'guniê', 'gupik', 'hipku', 'kapiê', 'kêpie', 'kêpin', 'kêpki', 'kingu', 'kipiê', 'kipnê', 'kpinê', 'kupiæ', 'kupie', 'kupiê', 'kupkê', 'kupki', 'kupni', 'kutiê', 'kuŸni', 'pêtku', 'piegu', 'piekê', 'piêdŸ', 'piknê', 'pikut', 'pinkê', 'pinku', 'puknê', 'punki', 'tupiê', 'ugiêæ', 'upiek', 'upiêæ', 'gupika', 'gupiki', 'gupiku', 'kuŸniê', 'piêknu', 'ukapiê', 'upiekê']
```

<a name="val"></a>
### Valid words (*find_certainly_valid_words*)
The last stage, which selects the final 'candidates' to put on the board, is to check whether the pre-selected word matches any of the patterns. At this stage, the moves (words) are evaluated to finally select the best-scoring ones.  

Each of the words is compared to each of the patterns. The position of the letter (or letters in the case of a bridge) is checked (from the pattern) in the examined word, if it (or their) is missing then the word is obviously rejected. Then check whether the word matches the structure of the pattern, i.e. whether the number of letters on the left and right matches the values from the pattern. If so, the value of the move is evaluated (based on the coordinates from the pattern and according to the official rules of the game - type of fields) and the word is added to the final list of words from which the best is selected.  

For this case, the program returned a list of 131 words (first is the word, second is the pattern and the last one is a score of the move):
```
[(('ukapiê', ('a', 3, 2, 2, 5, 'h')), 32), (('gapiê', ('a', 3, 2, 2, 5, 'h')), 26), (('gapê', ('a', 3, 2, 2, 5, 'h')), 24), (('gaiku', ('a', 3, 2, 2, 5, 'h')), 24), (('ugiêæ', ('æ', 9, 5, 5, 2, 'h')), 24), (('g¿ê', ('¿', 1, 9, 6, 1, 'h')), 23), (('g¿ê', ('¿', 1, 9, 5, 2, 'h')), 23), (('kaŸ', ('a', 3, 2, 1, 5, 'h')), 22), (('paŸ', ('a', 3, 2, 1, 5, 'h')), 22), (('Ÿga', ('a', 5, 6, 3, 0, 'v')), 22), (('Ÿga', ('a', 8, 5, 3, 0, 'h')), 22), (('gapiê', ('a', 3, 2, 1, 5, 'h')), 22), (('gapiu', ('a', 3, 2, 2, 5, 'h')), 22), (('kapiê', ('a', 3, 2, 2, 5, 'h')), 22), (('Ÿga', ('a', 3, 2, 2, 5, 'h')), 21), (('giêæ', ('æ', 9, 5, 4, 3, 'h')), 21), (('upiêæ', ('æ', 9, 5, 5, 2, 'h')), 21), (('¿uk', ('¿', 1, 9, 4, 2, 'h')), 20), (('¿up', ('¿', 1, 9, 4, 2, 'h')), 20), (('gapê', ('a', 3, 2, 1, 5, 'h')), 20), (('kapê', ('a', 3, 2, 2, 5, 'h')), 20), (('pakê', ('a', 3, 2, 2, 5, 'h')), 20), (('ukap', ('a', 3, 2, 2, 5, 'h')), 20), (('kapiê', ('a', 3, 2, 1, 5, 'h')), 20), (('kupiæ', ('æ', 9, 5, 5, 2, 'h')), 20), (('g¿ê', ('¿', 1, 9, 4, 2, 'h')), 19), (('akiê', ('a', 3, 2, 2, 5, 'h')), 18), (('gaik', ('a', 3, 2, 2, 5, 'h')), 18), (('kapê', ('a', 3, 2, 1, 5, 'h')), 18), (('pakê', ('a', 3, 2, 1, 5, 'h')), 18), (('piêæ', ('æ', 9, 5, 4, 3, 'h')), 18), (('upiæ', ('æ', 9, 5, 4, 3, 'h')), 18), (('gaiku', ('a', 3, 2, 1, 5, 'h')), 18), (('gapiu', ('a', 3, 2, 1, 5, 'h')), 18), (('ugiêæ', ('æ', 9, 5, 4, 3, 'h')), 18), (('kuæ', ('æ', 9, 5, 5, 2, 'h')), 17), (('giêæ', ('æ', 9, 5, 5, 2, 'h')), 17), (('upiêæ', ('æ', 9, 5, 4, 3, 'h')), 17), (('i¿', ('¿', 1, 9, 5, 2, 'h')), 16), (('aigu', ('a', 3, 2, 0, 5, 'h')), 14), (('akiê', ('a', 3, 2, 1, 5, 'h')), 14), (('kapu', ('a', 3, 2, 1, 5, 'h')), 14), (('paku', ('a', 3, 2, 1, 5, 'h')), 14), (('g¿ê', ('¿', 1, 9, 3, 2, 'h')), 13), (('kiæ', ('æ', 9, 5, 4, 3, 'h')), 13), (('piæ', ('æ', 9, 5, 4, 3, 'h')), 13), (('¿upê', ('¿', 2, 2, 2, 5, 'h')), 13), (('gupika', ('a', 5, 6, 5, 0, 'v')), 13), (('gupika', ('a', 8, 5, 5, 0, 'h')), 13), (('agê', ('a', 3, 2, 1, 5, 'h')), 12), (('Ÿga', ('a', 5, 6, 2, 0, 'v')), 12), (('Ÿga', ('a', 8, 5, 2, 0, 'h')), 12), (('aigu', ('a', 3, 2, 2, 5, 'h')), 12), (('gaik', ('a', 3, 2, 1, 5, 'h')), 12), (('kupa', ('a', 8, 5, 4, 0, 'h')), 11), (('pêka', ('a', 5, 6, 3, 0, 'v')), 11), (('pêka', ('a', 8, 5, 3, 0, 'h')), 11), (('puka', ('a', 5, 6, 4, 0, 'v')), 11), (('puka', ('a', 8, 5, 4, 0, 'h')), 11), (('hê', ('h', 7, 8, 0, 7, 'v')), 10), (('gap', ('a', 3, 2, 1, 5, 'h')), 10), (('hip', ('h', 7, 8, 1, 6, 'v')), 10), (('huk', ('h', 7, 8, 1, 6, 'v')), 10), (('idŸ', ('d', 2, 12, 1, 2, 'h')), 10), (('phu', ('h', 7, 8, 1, 6, 'v')), 10), (('¿uk', ('¿', 1, 9, 3, 2, 'h')), 10), (('¿up', ('¿', 1, 9, 3, 2, 'h')), 10), (('agiu', ('a', 3, 2, 1, 5, 'h')), 10), (('huki', ('h', 7, 8, 0, 7, 'v')), 9), (('kupa', ('a', 5, 6, 3, 0, 'v')), 9), (('kupa', ('a', 8, 5, 3, 0, 'h')), 9), (('puka', ('a', 5, 6, 3, 0, 'v')), 9), (('puka', ('a', 8, 5, 3, 0, 'h')), 9), (('têgi', ('t', 7, 7, 0, 7, 'v')), 9), (('tikê', ('t', 7, 7, 1, 6, 'v')), 9), (('tukê', ('t', 7, 7, 1, 6, 'v')), 9), (('¿uki', ('¿', 2, 2, 2, 5, 'h')), 9), (('hipku', ('h', 7, 8, 0, 7, 'v')), 9), (('i¿', ('¿', 1, 9, 4, 2, 'h')), 8), (('agi', ('a', 3, 2, 0, 5, 'h')), 8), (('dêg', ('d', 2, 12, 0, 2, 'h')), 8), (('gai', ('a', 3, 2, 1, 5, 'h')), 8), (('ghi', ('h', 7, 8, 1, 6, 'v')), 8), (('g¿ê', ('¿', 2, 2, 2, 5, 'h')), 8), (('¿up', ('¿', 1, 9, 2, 2, 'h')), 8), (('kipa', ('a', 5, 6, 5, 0, 'v')), 8), (('kipa', ('a', 8, 5, 5, 0, 'h')), 8), (('piêæ', ('æ', 9, 5, 3, 4, 'h')), 8), (('pika', ('a', 5, 6, 5, 0, 'v')), 8), (('pika', ('a', 8, 5, 5, 0, 'h')), 8), (('têpi', ('t', 7, 7, 0, 7, 'v')), 8), (('tikê', ('t', 7, 7, 0, 7, 'v')), 8), (('¿uki', ('¿', 2, 2, 1, 5, 'h')), 8), (('¿uk', ('¿', 1, 9, 1, 2, 'h')), 7), (('¿up', ('¿', 2, 2, 1, 5, 'h')), 7), (('¿up', ('¿', 1, 9, 1, 2, 'h')), 7), (('ekip', ('e', 7, 13, 0, 7, 'v')), 7), (('epik', ('e', 7, 13, 0, 7, 'v')), 7), (('kipa', ('a', 5, 6, 4, 0, 'v')), 7), (('kipa', ('a', 5, 6, 3, 0, 'v')), 7), (('kipa', ('a', 8, 5, 4, 0, 'h')), 7), (('kipa', ('a', 8, 5, 3, 0, 'h')), 7), (('pika', ('a', 5, 6, 4, 0, 'v')), 7), (('pika', ('a', 5, 6, 3, 0, 'v')), 7), (('pika', ('a', 8, 5, 4, 0, 'h')), 7), (('pika', ('a', 8, 5, 3, 0, 'h')), 7), (('tiku', ('t', 7, 7, 1, 6, 'v')), 7), (('ag', ('a', 3, 2, 0, 5, 'h')), 6), (('au', ('a', 3, 2, 0, 5, 'h')), 6), (('hê', ('h', 7, 8, 1, 6, 'v')), 6), (('hi', ('h', 7, 8, 1, 6, 'v')), 6), (('hu', ('h', 7, 8, 1, 6, 'v')), 6), (('hu', ('h', 7, 8, 0, 7, 'v')), 6), (('i¿', ('¿', 2, 2, 2, 5, 'h')), 6), (('i¿', ('¿', 1, 9, 6, 1, 'h')), 6), (('i¿', ('¿', 1, 9, 3, 2, 'h')), 6), (('i¿', ('¿', 1, 9, 2, 2, 'h')), 6), (('kia', ('a', 3, 2, 2, 5, 'h')), 5), (('kuæ', ('æ', 9, 5, 2, 4, 'h')), 5), (('nip', ('n', 5, 12, 0, 2, 'h')), 5), (('pai', ('a', 3, 2, 2, 5, 'h')), 5), (('pak', ('a', 3, 2, 2, 5, 'h')), 5), (('paŸ', ('a', 3, 2, 2, 5, 'h')), 5), (('pia', ('a', 5, 6, 5, 0, 'v')), 5), (('pia', ('a', 5, 6, 4, 0, 'v')), 5), (('pia', ('a', 8, 5, 5, 0, 'h')), 5), (('pia', ('a', 8, 5, 4, 0, 'h')), 5), (('pia', ('a', 3, 2, 2, 5, 'h')), 5), (('tiu', ('t', 7, 7, 1, 6, 'v')), 5), (('tuk', ('t', 7, 7, 0, 7, 'v')), 5), (('tup', ('t', 7, 7, 0, 7, 'v')), 5), (('¿uk', ('¿', 2, 2, 0, 5, 'h')), 5), (('¿uk', ('¿', 1, 9, 0, 2, 'h')), 5), (('¿up', ('¿', 2, 2, 0, 5, 'h')), 5), (('¿up', ('¿', 1, 9, 0, 2, 'h')), 5), (('kpiæ', ('æ', 9, 5, 3, 4, 'h')), 5), (('dip', ('d', 2, 12, 0, 2, 'h')), 3), (('kia', ('a', 5, 6, 2, 0, 'v')), 3), (('kia', ('a', 8, 5, 2, 0, 'h')), 3), (('kiæ', ('æ', 9, 5, 2, 4, 'h')), 3), (('pia', ('a', 5, 6, 2, 0, 'v')), 3), (('pia', ('a', 8, 5, 2, 0, 'h')), 3), (('piæ', ('æ', 9, 5, 2, 4, 'h')), 3), (('tik', ('t', 7, 7, 0, 7, 'v')), 3), (('tui', ('t', 7, 7, 1, 6, 'v')), 3), (('hi', ('h', 7, 8, 0, 7, 'v')), 2), (('ka', ('a', 5, 6, 1, 0, 'v')), 2), (('ka', ('a', 8, 5, 1, 0, 'h')), 2), (('ka', ('a', 3, 2, 1, 5, 'h')), 2), (('pa', ('a', 5, 6, 1, 0, 'v')), 2), (('pa', ('a', 8, 5, 1, 0, 'h')), 2), (('pa', ('a', 3, 2, 1, 5, 'h')), 2), (('tê', ('t', 7, 7, 1, 6, 'v')), 2), (('tu', ('t', 7, 7, 1, 6, 'v')), 2), (('ag', ('a', 3, 2, 1, 5, 'h')), 1), (('au', ('a', 3, 2, 1, 5, 'h')), 1), (('id', ('d', 2, 12, 1, 2, 'h')), 1), (('ii', ('i', 3, 12, 0, 2, 'h')), 1), (('i¿', ('¿', 2, 2, 1, 5, 'h')), 1), (('i¿', ('¿', 1, 9, 1, 2, 'h')), 1)]
```
 <a name="fin"></a>
 ## Final Result
Value of the best move was 32 points and according to the pattern assigned to the best word, the word is putted on the board:
<p align="center">
  <img src="https://i.imgur.com/Hhfp4Tb.png" width=40% alt="Img"/>
</p>

 <a name="stat"></a>
# Status
The plans are to add additional, more complex, but less popular types of moves - adding letters to existing words, arranging several words at once. These could be done by creating new types of patterns and a little changes in algorithm engine. Feel free to pull request.  

Also an improvement should be made to create bridges so that they can be created not only from letters that belong to *right angles*, but also other letters from the board - in this example *ê* is not *right angle* and bridge exist, but program will not find it:
<p align="center">
  <img src="https://i.imgur.com/gkaJ25M.png" width=32% alt="Img"/>
</p>
                                                       
3-letter (and more) bridges should also be included, because they are not currently found:
<p align="center">
  <img src="https://i.imgur.com/OyE6Wg2.png" width=40% alt="Img"/>
</p>
