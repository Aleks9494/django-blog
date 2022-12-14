Documentation for the implemented API. <br>
Includes routes and their methods, input and output data, examples of requests and responses. <br>
It is also possible to see the SWAGGER documentation for the route 'localhost/swagger/'. <br>
Django admin is also implemented for ease of viewing and managing users and content. <br>


1) <b>/api/v1/auth/users/</b>

	New User Registration, method = POST.
	Unique email field, authorization is based on it.
	
	Input data - UserCreate{<br>
			- username* - string<br>
			title: Имя, maxLength: 50, minLength: 1<br>
		 	- email* - string($email)<br>
			title: Емайл, maxLength: 255, minLength: 1<br>
			- password* - string<br>
			title: Password, minLength: 1<br>
		 	}<br>
		 
	Examples:<br>
	
	1) input data -  
		{
	  "username": "Test_User",
	  "email": "user@example.com",
	  "password": "password55648415"
	}	
	
	response - status code 201, 
		{
	  "username": "Test_User",
	  "email": "user@example.com",
	  "id": 1194<br>
	}
	
	2) input data -  
		{
	  "username": "Test_User_1",
	  "email": "user@example.com",
	  "password": "password55648415"
	}
	
	response - status code 400,
		{
		  "email": [
		    	"Пользователь с таким Емайл уже существует."
		  ]
	}
	
	3) input data -  
		{
	  "username": "Test_User_1",
	  "email": "user_2@example.com",
	  "password": "password"
	}
	
	response - status code 400, 
		{
  		"password": [
    			"Введённый пароль слишком широко распространён."
  		]
	}	
	
	4) input data -  
		{
	  "email": "user_2@example.com",
	  "password": "password"
	}
	
	response - status code 400, 
		{
  		"username": [
    			"Обязательное поле."
  		]
	}
	
2) <b>/api/v1/token/login/</b>

	Authorization of a registered user, obtaining a token for further actions in API.
	Method - POST. <br>	
	Input data - TokenCreate{ <br>
		- password - string<br>
		title: Password, minLength: 1<br>
		- email - string<br>
		title: Email, minLength: 1<br>
	} <br>
	
	Examples:<br>

	1) input data -  
		{
	  "email": "user@example.com",
	  "password": "password55648415"
	}	
	
	response - status code 200, 
	  	{
  		"auth_token": "d1536f949289800f64c7c715f7e8a1f9fe9d17c5"
		}
		
	2) input data -  
		{
	  "email": "user_1@example.com",
	  "password": "password55648415"
	}	
	
	response - status code 400,
		{
  	"non_field_errors": [
    		"Невозможно войти с предоставленными учетными данными."
  		]
	}
	
3) <b>/api/v1/token/logout/</b>
	
	Logged out user, method - POST
	Input data - None.
	Request headers must contain header «Authorizathion»: «Token ...». <br>
	
	Examples: <br>
	
	1) header present with valid token - response, status code 204 <br>
	
	2) header present, token not valid - response, status code 403 <br>
		{
    			"detail": "Недопустимый токен."
		}
		
	3) no header - response, status code 403 <br>
		{
    			"detail": "Учетные данные не были предоставлены."
		}	
	
4) <b>/api/v1/users</b>
	
	View a list of other users besides yourself and the admin. Method - GET.
	Only for authorized users.
	(Request headers must contain header «Authorizathion»: «Token ...»).
	Ability to sort by number of posts.
	Input data - None. <br>
	
	Examples: <br>
	
	1) header present, token not valid - response, status code 403 <br>
		{
    			"detail": "Недопустимый токен."
		}
		
	2) no header - response, status code 403 <br>
		{
    			"detail": "Учетные данные не были предоставлены."
		}
	
	3) header present with valid token - response, status code 200 <br>	
		[
	    {
		"id": 57,
		"username": "DDDDDD",
		"email": "6@mail.ri",
		"time_create": "2022-08-04T13:55:07.543221+03:00",
		"number_of_posts": 0
	    }, <br>
	    {
		"id": 3,
		"username": "Kostya",
		"email": "3@mail.ru",
		"time_create": "2022-08-02T10:55:50.871202+03:00",
		"number_of_posts": 2
	    }, <br>
	    {
		"id": 4,
		"username": "Maxim",
		"email": "4@mail.ru",
		"time_create": "2022-08-02T10:56:19.347405+03:00",
		"number_of_posts": 1
	    }, <br>
	    {
		"id": 2,
		"username": "Sasha",
		"email": "2@mail.ru",
		"time_create": "2022-08-02T10:55:13.353442+03:00",
		"number_of_posts": 1
	    }, <br>
	    {
		"id": 5,
		"username": "Slava",
		"email": "5@mail.ru",
		"time_create": "2022-08-02T11:08:40.796538+03:00",
		"number_of_posts": 4
	    }
	]	
	
	4) sorting by number of posts - api/v1/users?ordering=-number_of_posts		
			
		[
	    {
		"id": 5,
		"username": "Slava",
		"email": "5@mail.ru",
		"time_create": "2022-08-02T11:08:40.796538+03:00",
		"number_of_posts": 4
	    }, <br>
	    {
		"id": 3,
		"username": "Kostya",
		"email": "3@mail.ru",
		"time_create": "2022-08-02T10:55:50.871202+03:00",
		"number_of_posts": 2
	    }, <br>
	    {
		"id": 4,
		"username": "Maxim",
		"email": "4@mail.ru",
		"time_create": "2022-08-02T10:56:19.347405+03:00",
		"number_of_posts": 1
	    }, <br>
	    {
		"id": 2,
		"username": "Sasha",
		"email": "2@mail.ru",
		"time_create": "2022-08-02T10:55:13.353442+03:00",
		"number_of_posts": 1
	    }, <br>
	    {
		"id": 57,
		"username": "DDDDDD",
		"email": "6@mail.ri",
		"time_create": "2022-08-04T13:55:07.543221+03:00",
		"number_of_posts": 0
	    }
	]

5) <b>/api/v1/posts</b>
	
	Method - GET, POST.
	View a list of posts of other users, except for your own, sorted by the date. 
 	Create new post.
	Only for authorized users.
	(Request headers must contain header «Authorizathion»: «Token ...»), if it's missing - error 403.<br>
	Input data for method POST- {<br>
		- title* - string <br>
		title: Заголовок, maxLength: 100, minLength: 1 <br>
		- content* - string <br>
		title: Контент, minLength: 1 <br>
 		} <br>
 		
 		
 	method GET — output data:  id, title, content, time_create, author_email, hiddenfield author <br>
 	
	Examples: <br>
	 	[
	    {
		"id": 15,
		"title": "Post User 2",
		"content": "dsfsdfsdfsdf",
		"time_create": "2022-08-03T15:25:34.930296+03:00",
		"author_email": "2@mail.ru"
	    }, <br>
	    {
		"id": 9,
		"title": "Post User 5 again",
		"content": "22234343243333333332",
		"time_create": "2022-08-02T12:03:16.330073+03:00",
		"author_email": "5@mail.ru"
	    }, <br>
	    {
		"id": 7,
		"title": "Post User 5",
		"content": "22234343243333333332",
		"time_create": "2022-08-02T11:58:45.558509+03:00",
		"author_email": "5@mail.ru"
	    }, <br>
	    {
		"id": 5,
		"title": "Post user 3 again",
		"content": "DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD",
		"time_create": "2022-08-02T11:04:38.944181+03:00",
		"author_email": "3@mail.ru"
	    }, <br>
	    {
		"id": 4,
		"title": "Post user 4",
		"content": "VVVVVVVVVVVVVVVVVVVVVVVVVVVVV",
		"time_create": "2022-08-02T11:03:42.788053+03:00",
		"author_email": "4@mail.ru"
	    }, <br>
	    {
		"id": 2,
		"title": "Post User 3",
		"content": "PPPPPPPPPPPPPPPPPPPPPPPP",
		"time_create": "2022-08-02T10:58:42.714411+03:00",
		"author_email": "3@mail.ru"
	    } 
	]	<br>
	
	method POST <br>
	
	 - field title is unique <br>
	
	Examples: <br>

	1) input data -  <br>
		 {
        	"title": "Post Test_User",
        	"content": "Content of Post"
    	} <br>	
	
	response - status code 201, <br>
	  	{
		"id": 395,
		"title": "Post Test_User",
		"content": "Content of Post",
		"time_create": "2022-08-08T11:35:14.082955+03:00",
		"author_email": "user@example.com"	    
	} <br>
	
	response - status code 400, <br>
		{
    		"title": [
        		"Пост с таким Заголовок уже существует."
    		]
	}
	
	2) input data -  
		 {
        	"title": "Post Test_User again",
    	} <br>
	
	response - status code 400, 
		{
    		"content": [
        		"Обязательное поле."
    		]
	}

6) <b>/api/v1/posts/<int:post_id> </b>

	Add and delete a post to the user's subscriptions feed. Method - GET, DELETE.
	Only for authorized users.
	(Request headers must contain header «Authorizathion»: «Token ...»), if it's missing - error 403.
	Input data - None. <br>
	
	1) method GET <br>

		1) /api/v1/posts/15 <br>

		response - status code 200,	
		{
    		"message": "Post Post User 2 was added to your's subscriptions!!"
		}
	
		response - status code 400,
		{
    		"message": "You are already subscribed to this post!!"
		}	
	
		2) /api/v1/posts/289 <br>

		response - status code 404,
		{
    		"message": "Post matching query does not exist."
		}
	
	2) метод DELETE <br>

		1) /api/v1/posts/250 <br>

		response - status code 404,
		{
    		"message": "Subscriptions matching query does not exist."
		}
	
		2) /api/v1/posts/15 <br>

		response - status code 200,
		{
    		"message": "Post Post User 2 was deleted from your's subscriptions!!"
		}


7) <b>/api/v1/subs</b>

	Method - GET.
	View the feed of the user's subscriptions, sorting by the date the post was created.
	Pagination - 10 posts per page.
	Filtering by post read.
	Only for authorized users.
	Request headers must contain header «Authorizathion»: «Token ...»), if it's missing - error 403.
	Input data - None.<br>
	
	1) api/v1/subs <br>
	
	Examples: <br>
	
	response - status code 200, <br> 
	
	
	{
    "count": 25,   - total quantity of subscriptions <br>
    "next": http://127.0.0.1:8000/api/v1/subs?page=2, - next page on pagination <br>
    "previous": http://127.0.0.1:8000/api/v1/subs, - previos page on pagination <br>
    "results": [ <br>
        {
            "id": 167,
            "post": {
                "id": 9,
                "title": "Post User 5 again",
                "content": "22234343243333333332",
                "time_create": "2022-08-02T12:03:16.330073+03:00",
                "author_email": "5@mail.ru"
            },
            "readed": false
        }, <br>
        {
            "id": 166,
            "post": {
                "id": 7,
                "title": "Post User 5",
                "content": "22234343243333333332",
                "time_create": "2022-08-02T11:58:45.558509+03:00",
                "author_email": "5@mail.ru"
            },
            "readed": false
        }, <br>
        {
            "id": 165,
            "post": {
                "id": 5,
                "title": "Post user 3 again",
                "content": "DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD",
                "time_create": "2022-08-02T11:04:38.944181+03:00",
                "author_email": "3@mail.ru"
            },
            "readed": false
        }, <br>
        {
            "id": 164,
            "post": {
                "id": 4,
                "title": "Post user 4",
                "content": "VVVVVVVVVVVVVVVVVVVVVVVVVVVVV",
                "time_create": "2022-08-02T11:03:42.788053+03:00",
                "author_email": "4@mail.ru"
            },
            "readed": true
        }, <br>
        {
            "id": 163,
            "post": {
                "id": 2,
                "title": "Post User 3",
                "content": "PPPPPPPPPPPPPPPPPPPPPPPP",
                "time_create": "2022-08-02T10:58:42.714411+03:00",
                "author_email": "3@mail.ru"
            },
            "readed": false
        }, <br>
        .......
    ]
} <br>

	2) /api/v1/subs?readed=True <br>
	
	response - status code 200, <br>
	{
    "count": 1, <br>
    "next": null, <br>
    "previous": null, <br>
    "results": [ <br>
        {
            "id": 164,
            "post": {
                "id": 4,
                "title": "Post user 4",
                "content": "VVVVVVVVVVVVVVVVVVVVVVVVVVVVV",
                "time_create": "2022-08-02T11:03:42.788053+03:00",
                "author_email": "4@mail.ru"
            },
            "readed": true
        } <br>
    ]
} <br>


8) <b>/api/v1/subs/<int:sub_id></b>

	Method - GET, PUT.
	GET - View subscription and post in subscription.
	PUT -  Make a read mark of post.
	Only for authorized users.
	Request headers must contain header «Authorizathion»: «Token ...»), if it's missing - error 403.
	Input data - None. <br>
	
	1) method GET <br>
	
		1) /api/v1/subs/168 <br>
	
		{
	    	"id": 168, 
	    	"post": {
			"id": 15,
			"title": "Post User 2",
			"content": "dsfsdfsdfsdf",
			"time_create": "2022-08-03T15:25:34.930296+03:00",
			"author_email": "2@mail.ru"
		    },
		    "readed": false
		} <br>
	
		2) /api/v1/subs/261 <br>
	
		{
    			"detail": "Страница не найдена."
		} <br>
	
	2) method PUT <br>
	
		1) /api/v1/subs/261 <br>
	
		{
    			"detail": "Страница не найдена."
		} <br>
	
		2) /api/v1/subs/168 <br>
	
		input data - 
		{
  		"post": {
    			"title": "string",
   	 		"content": "string"
  		},
  		"readed": true
		} <br>
	
		- Post data is read-only and cannot be changed. <br>
	
		response - status code 200, 
			{
			  "id": 168,
			  "post": {
			    "id": 15,
			    "title": "Post User 2",
			    "content": "dsfsdfsdfsdf",
			    "time_create": "2022-08-03T15:25:34.930296+03:00",
			    "author_email": "2@mail.ru"
			  },
			  "readed": true
		} 
	
	
				
		 
