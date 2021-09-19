> ## ***/auth/register-student***  
> Create student account.  
> 
> ### Methods allowed  
> - POST
> 
> ### Fields required  
> - username: Student username.  
> - name: Name of the student.  
> - email: Email ID of the student.  
> - password: Password for the new account to be created.  
>  
> ### Return values
> - message: Error message if any exception is raised. Success message is the account is created suucessfully.  

> ## ***/auth/login***  
> Login into user account.  
> 
> ### Methods allowed  
> - POST
> 
> ### Fields required  
> - username: account username.   
> - password: Password of the account.  
>  
> ### Return values
> - token: User token if authentication was successful, error message if authentication failed.

> ## ***/auth/logout***  
> Logout from user account.  
> 
> ### Methods allowed  
> - POST
> 
> ### Fields required  
> token: Token of the user  
>  
> ### Return values
> - None

> ## ***/auth/register-university***  
> Create university account.  
> 
> ### Methods allowed  
> - POST
> 
> ### Fields required  
> - username: Unique identification username for the university.  
> - name: Name of the University.  
> - email: Email ID of the university.  
> - password: Password for the new account to be created.  
>  
> ### Return values
> - message: Error message if any exception is raised. Success message is the account is created suucessfully. 
