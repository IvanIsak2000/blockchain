<div id = "header" align="center">
<img src = "https://github.com/IvanIsak2000/blockchain-app/blob/master/logo.png"/>
<br>
</div>


EN
==

BASIC
--
This is a program for creating a simple local Blockchain!


FUNCTONS
--

1. Create a blocks
2. Integrity check 
3. Database maintenance


EXAMPLE
--

## CREATE


**Do you want to create your own local blockchain?**

<p>
1. Select mode: number 1 = create, number 2 = check all blocks
 
![image](https://user-images.githubusercontent.com/79650307/226310262-af6dee09-4243-4b73-810e-d0c0776233fd.png)
``I select 1``
</p>

<p>
2. Fill in the data
  
![image](https://user-images.githubusercontent.com/79650307/226311651-295d90f1-ef6c-4d7b-9fb2-83b98793d2bd.png)
   ``I wrote name Ivan, amount = 200 , to whom = Putin``
</p>

<p>
3. All done
  
  ![image](https://user-images.githubusercontent.com/79650307/226313395-46d9ecc3-6d81-4568-8c5d-ed826c68ec69.png)

</p>


## CHECK
Okay, you created the second block (the first block is created automatically - genesis block) and you want to check the integrity of your blockchain?

### True
<p>
  To check, reopen the program and enter the number 2 
  
![image](https://user-images.githubusercontent.com/79650307/226314998-fdb32b69-86d1-4df3-b1b0-d72990a734cd.png)
  ``True, so the hashes written to the database match the hashes of their transactions folder  ``
</p>

<hr/>

### False
<p>
  True is clear, but how to get a message that the blockchain has been changed?

1. Open folder ``transactions`` and open any transaction and add something
  
  ![image](https://user-images.githubusercontent.com/79650307/226316821-0cd9771b-eec1-4a53-a540-40fa31f10756.png)


2. Open the program and check with number 2 - the program will show ``False``.
  
  ![image](https://user-images.githubusercontent.com/79650307/226316933-098d3df7-6ff3-41f8-8c73-2c136c0456d7.png)

  </p>
