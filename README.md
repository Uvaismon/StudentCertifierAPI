> ## ***/auth/register/<user_type>***  
> Create user account.  
> 
> ### Methods allowed  
> - POST
>
> ### user_type
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
> Type of user account. Allowed values are (student, university)  
> 
> ### Fields required  
> - username: user username.  
> - name: Name of the user.  
> - email: Email ID of the user.  
> - password: Password for the new account to be created.  
>  
> ### Return values
> - message: Error message if any exception is raised. Success message if the account is created suucessfully. 
> - result: 1, if account created successfully, 0 otherwise.   

> ## ***/auth/login/<user_type>***  
> Login into user account.  
> 
> ### Methods allowed  
> - POST
>
> ### user_type
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
>Type of user account. Allowed values are (student, university)
> 
> ### Fields required  
> - username: account username.   
> - password: Password of the account.  
>  
> ### Return values
> - token: User token if authentication was successful, error message if authentication failed.
> - result: 1, if the authentication was successful, 0 otherwise.  

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

> ## ***/cert/certificate-request***  
> Students request for certificate.  
>
> ### Methods allowed  
> - POST  
>
> ### Fields required  
> - token: Authentication token.  
> - university: University code, same as university username.  
> - course: Name of the course completed.  
> grade_obtained: Grade obtained in the course.  
>
> ### Return values
> - message: Error message if any, success message if the request was successful.  
> - result: 1, if the request was successful, 0 otherwise.  