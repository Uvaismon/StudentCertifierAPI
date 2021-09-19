> ## ***/auth/register-student***  
> Create student account.  
> 
> ### Methods allowed  
> - POST
> 
> ### Fields required  
> - usn: Student identification number.  
> - name: Name of the student.  
> - email: Email ID of the student.  
> - password: Password for the new account to be created.  
>  
> ### Return values
> - message: Error message if any exception is raised. Success message is the account is created suucessfully.  

> ## ***/auth/login-student***  
> Login into student account.  
> 
> ### Methods allowed  
> - POST
> 
> ### Fields required  
> - usn: Student identification number.   
> - password: Password of the student account.  
>  
> ### Return values
> - token: User token if authentication was successful, error message if authentication failed.

> ## ***/auth/logout-student***  
> Logout from student account.  
> 
> ### Methods allowed  
> - POST
> 
> ### Fields required  
> token: Token of the user  
>  
> ### Return values
> - None
