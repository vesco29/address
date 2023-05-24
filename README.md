# Development task

Given a list of people and their addresses, create a script in python3 that
groups people who live at the same address.

### Input

1) A path to a utf-8 encoded .csv file with two columns Name,Address.
2) A path to a directory where output file should be saved.
***
### Output

A text document saved at the specified location. Each line is a commaseparated list of names of the people living at the same address. The
names in a line should be sorted alphabetically. The lines of the file should
also be sorted alphabetically.
***
#### Example input file data
```
Example input file data*
Name,Address
Ivan Draganov,”ul. Shipka 34, 1000 Sofia, Bulgaria”
Leon Wu,”1 Guanghua Road, Beijing, China 100020”
Ilona Ilieva,”ул. Шипка 34, София, България”
Dragan Doichinov,”Shipka Street 34, Sofia, Bulgaria”
Li Deng,”1 Guanghua Road, Chaoyang District, Beijing, P.R.C 100020”
Frieda Müller,”Konrad-Adenauer-Straße 7, 60313 Frankfurt am Main,
Germany”
```
#### Expected output
```
Dragan Doichinov, Ilona Ilieva, Ivan Draganov
Frieda Müller
Leon Wu, Li Deng
```
### Additional requirements
1) Observe good coding practices
2) Include a short readme file documenting the solution.
3) There are no library usage restrictions.

