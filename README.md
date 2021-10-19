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
> - result: 1, if account created successfully, otherwise 0.   

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
> - result: 1, if the authentication was successful, otherwise 0.  

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

> ## ***/cert/certificate-request***  (deprecated)
> Students request for certificate.  
>
> ### Methods allowed  
> - POST  
>
> ### Fields required  
> - token: Authentication token.  
> - university: University code, same as university username.  
> - course: Name of the course completed.  
> - grade_obtained: Grade obtained in the course.  
>
> ### Return values
> - message: Error message if any, success message if the request was successful.  
> - result: 1, if the request was successful, 2 if the user does not belong to the university, 3 if the user is not enrolled in any course, 0 if other error occured.  

> ## ***/cert/certificate-approve***  
> Universities generates certificates using this endpoint.
>
> ### Methods allowed  
> - POST
> ### Fieds required
> - certificate_id: ID of the certification request made by the student.   
> - token: University authentication token.  
>
> ### Return values
> - message: Error message if any, success message if the request was successful.  
> - result: 1, if the request was successful, otherwise 0.  

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
> Get the list of certificate maintained my a university.  
>
> ### Methods allowed  
> - GET  
>
> ### Fields required
> - university_code: username of univeristy account.
> - certified: A boolean value. Fetches only certified certificate numbers if set true, otherwise fetches uncertified certificate number.  
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
> - certified: A boolean value. Fetches only certified certificate numbers if set true, otherwise fetches uncertified certificate number.  
>
> ### Return values
> Return a list of certificate IDs.  
> - certificate_id: ID of the certificates  

> ## ***cert/certificate-verification***  
> Upload a certificate to check the integrity of the certificate.
> ### Methods allowed
> - POST
>
> ### Fields required  
> - certificate: Certificate pdf file.
> - certificate_id: ID of the certificate uploaded.  
>
> ### Return value
> - message: Message denoting if the certificate is valid or not.  
> - result: 1, if the request was successful, otherwise 0.  

> ## ***cert/certificate-details-list-student***  
> Returns a list of certificate details of a given student.  
>
> ### Methods allowed  
> - POST  
>
> ### Fields required  
> - student: username of student account.
> - certified: A boolean value. Fetches only certified certificate numbers if set true, otherwise fetches uncertified certificate number.
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

> ## ***cert/certificate-details-list-university***  
> Returns a list of certificate details of a given university.  
>
> ### Methods allowed  
> - POST  
>
> ### Fields required  
> - university_code: username of university account.
> - certified: A boolean value. Fetches only certified certificate numbers if set true, otherwise fetches uncertified certificate number.
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

> ## ***/cert/estimate-fee***  
> Estimate the transaction fee.  
> 
> ### Methods allowed  
> - GET  
> 
> ### Fields required  
> none 
>  
> ### Return values  
> - fee: Estimated fee of the transaction in US dollars.

> ## ***/cert/certificate-request-student***  
> Students request for certificate.  
>
> ### Methods allowed  
> - POST  
>
> ### Fields required  
> - token: Authentication token.  
> - student_id: Student ID as per university database.  
>
> ### Return values
> - message: Error message if any, success message if the request was successful.  
> - result: 
>   - 1, if the request was successful.  
>   - 2, if the user does not belong to the university.  
>   - 3, if the user is not enrolled in any course.   
>   - 4, if the course is incomplete.  
>   - 5, if already requested for the certificate.  
>   - 6, if already certified for the course.  
>   - 0, if other error occured.

> ## ***/cert/certificate-reject***  
> Admin reject certificate request fromt students.  
>
> ### Methods allowed
> - POST
>
> ### Fields required  
> - token: Token of the university account.  
> - certificate_id: ID of the certificate request to be rejected.  
>
> ### Return values
> - result: 1, if the rejection was successful, 0 otherwise.
> - message:  Error message if any, success message if the request was successful.  