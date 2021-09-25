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

> ## ***/cert/certificate-approve***  
> Universities generates certificates using this endpoint.
>
> ### Methods allowed  
> - POST
> ### Fieds required
> - certificate_id: ID of the certification request make by the student.   
> - token: University authentication token.  
>
> ### Return values
> - message: Error message if any, success message if the request was successful.  
> - result: 1, if the request was successful, 0 otherwise.  

> ## ***/cert/certificate-details***  
> Fetch certificate details.  
>
> ### Methods allowed  
> - GET
>
> ### Fields required  
> - certificate_id: ID of the certificate to fetch the details.  
>
> ### Return values  
> Returns a list of json objects.
> - certificate_id: ID of the certificate.  
> - student: Name of the student.  
> - university: Name of the university.  
> - course: Name of the course completed.  
> - grade_obtained: Grade obtained in the course.  
> - certified_on: Certificate generation data.
> - certificate_link: Certificate download link.  
> - certified: A bool value denoting if the certificate is generated or not.  

> ## ***cert/certificate-list-university***
> Get the list of certificate maintained my an university.  
>
> ### Methods allowed  
> - GET  
>
> ### Fields required
> - university_code: username of univeristy account.
> - certified: A boolean value. Fetched only certified certificate numbers if set true, otherwise fetched uncertified certificate number.  
>
> ### Return values
> Return a list of certificate IDs.  
> - certificate_id: ID of the certificate  

> ## ***cert/certificate-list-student***
> Get the list of certificate linked to a student.  
>
> ### Methods allowed  
> - GET  
>
> ### Fields required
> - student: username of student account.
> - certified: A boolean value. Fetched only certified certificate numbers if set true, otherwise fetched uncertified certificate number.  
>
> ### Return values
> Return a list of certificate IDs.  
> - certificate_id: ID of the certificate  

> ## ***cert/certificate-verification***  
> Upload a certificate to check the integrity of the certificate.
> ### Method allowed
> - POST
>
> ### Fields required  
> certificate: Certificate pdf file.
> certificate_id: ID of the certificate uploaded.  
>
> ### Return value
> - message: Message denoting if the certificate is valid or not.  
> - result: 1, if the request was successful, 0 otherwise.  

> ## ***cert/certificate-details-list-student***  
> Returns a list of certificate details of a given student.  
>
> ### Method allowed  
> - POST  
>
> ### Fields required  
> - student: username of student account.
> - certified: A boolean value. Fetched only certified certificate numbers if set true, otherwise fetched uncertified certificate number.
>
> ### Return value  
> Returns a list of json objects.
> - certificate_id: ID of the certificate.  
> - student: Name of the student.  
> - university: Name of the university.  
> - course: Name of the course completed.  
> - grade_obtained: Grade obtained in the course.  
> - certified_on: Certificate generation data.
> - certificate_link: Certificate download link.  
> - certified: A bool value denoting if the certificate is generated or not.   