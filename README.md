Documentation for the implemented API.
Includes routes and their methods, input and output data, examples of requests and responses.
It is also possible to see the SWAGGER documentation for the route 'localhost/swagger/'
Django admin is also implemented for ease of viewing and managing users and content.


1) /api/v1/auth/users/

	New User Registration, method = POST
	Unique email field, authorization is based on it
	input data - UserCreate{
			- username* - string
			title: Имя, maxLength: 50, minLength: 1
		 	- email* - string($email)
			title: Емайл, maxLength: 255, minLength: 1
			- password* - string
			title: Password, minLength: 1
		 	}
		 
	Examples:
	
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
	  "id": 1194
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
  		""username": [
    			"Обязательное поле."
  		]
	}
	
2) /api/v1/token/login/

	Authorization of a registered user, obtaining a token for further actions in API.
	Method - POST	
	input data - TokenCreate{
		- password - string
		title: Password, minLength: 1
		- email - string
		title: Email, minLength: 1
	}
	
	Examples:

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
	
3) /api/v1/token/logout/
	
	Logged out user, method - POST
	Input data - None
	Request headers must contain header «Authorizathion»: «Token ...»
	
	Examples:
	
	1) header present with valid token - response, status code 204
	
	2) header present, token not valid - response, status code 403
		{
    			"detail": "Недопустимый токен."
		}
		
	3) no header - response, status code 403
		{
    			"detail": "Учетные данные не были предоставлены."
		}	
	
4) /api/v1/users
	
	View a list of other users besides yourself and the admin. Method - GET/
	Only for authorized users
	(Request headers must contain header «Authorizathion»: «Token ...»)
	Ability to sort by number of posts
	Input data - None
	
	Examples: 
	
	1) header present, token not valid - response, status code 403
		{
    			"detail": "Недопустимый токен."
		}
		
	2) no header - response, status code 403
		{
    			"detail": "Учетные данные не были предоставлены."
		}
	
	3) header present with valid token - response, status code 200
			
		[
	    {
		"id": 57,
		"username": "DDDDDD",
		"email": "6@mail.ri",
		"time_create": "2022-08-04T13:55:07.543221+03:00",
		"number_of_posts": 0
	    },
	    {
		"id": 3,
		"username": "Kostya",
		"email": "3@mail.ru",
		"time_create": "2022-08-02T10:55:50.871202+03:00",
		"number_of_posts": 2
	    },
	    {
		"id": 4,
		"username": "Maxim",
		"email": "4@mail.ru",
		"time_create": "2022-08-02T10:56:19.347405+03:00",
		"number_of_posts": 1
	    },
	    {
		"id": 2,
		"username": "Sasha",
		"email": "2@mail.ru",
		"time_create": "2022-08-02T10:55:13.353442+03:00",
		"number_of_posts": 1
	    },
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
	    },
	    {
		"id": 3,
		"username": "Kostya",
		"email": "3@mail.ru",
		"time_create": "2022-08-02T10:55:50.871202+03:00",
		"number_of_posts": 2
	    },
	    {
		"id": 4,
		"username": "Maxim",
		"email": "4@mail.ru",
		"time_create": "2022-08-02T10:56:19.347405+03:00",
		"number_of_posts": 1
	    },
	    {
		"id": 2,
		"username": "Sasha",
		"email": "2@mail.ru",
		"time_create": "2022-08-02T10:55:13.353442+03:00",
		"number_of_posts": 1
	    },
	    {
		"id": 57,
		"username": "DDDDDD",
		"email": "6@mail.ri",
		"time_create": "2022-08-04T13:55:07.543221+03:00",
		"number_of_posts": 0
	    }
	]

5) /api/v1/posts
	
	Method - GET, POST
	View a list of posts of other users, except for your own, sorted by the date. 
 	Create new post
	Only for authorized users
	(Request headers must contain header «Authorizathion»: «Token ...»), if it's missing - error 403
	Input data for method POST- {
		- title* - string
		title: Заголовок, maxLength: 100, minLength: 1
		- content* - string
		title: Контент, minLength: 1
 		}
 		
 		
 	method GET — output data:  id, title, content, time_create, author_email, hiddenfield author
 	
	Examples:
	 	[
	    {
		"id": 15,
		"title": "Post User 2",
		"content": "dsfsdfsdfsdf",
		"time_create": "2022-08-03T15:25:34.930296+03:00",
		"author_email": "2@mail.ru"
	    },
	    {
		"id": 9,
		"title": "Post User 5 again",
		"content": "22234343243333333332",
		"time_create": "2022-08-02T12:03:16.330073+03:00",
		"author_email": "5@mail.ru"
	    },
	    {
		"id": 7,
		"title": "Post User 5",
		"content": "22234343243333333332",
		"time_create": "2022-08-02T11:58:45.558509+03:00",
		"author_email": "5@mail.ru"
	    },
	    {
		"id": 5,
		"title": "Post user 3 again",
		"content": "DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD",
		"time_create": "2022-08-02T11:04:38.944181+03:00",
		"author_email": "3@mail.ru"
	    },
	    {
		"id": 4,
		"title": "Post user 4",
		"content": "VVVVVVVVVVVVVVVVVVVVVVVVVVVVV",
		"time_create": "2022-08-02T11:03:42.788053+03:00",
		"author_email": "4@mail.ru"
	    },
	    {
		"id": 2,
		"title": "Post User 3",
		"content": "PPPPPPPPPPPPPPPPPPPPPPPP",
		"time_create": "2022-08-02T10:58:42.714411+03:00",
		"author_email": "3@mail.ru"
	    }
	]	
	
	method POST 
	
	 - field title is unique
	
	Examples:

	1) input data -  
		 {
        	"title": "Post Test_User",
        	"content": "Content of Post"
    	}	
	
	response - status code 201, 
	  	{
		"id": 395,
		"title": "Post Test_User",
		"content": "Content of Post",
		"time_create": "2022-08-08T11:35:14.082955+03:00",
		"author_email": "user@example.com"	    
	}
	
	response - status code 400,
		{
    		"title": [
        		"Пост с таким Заголовок уже существует."
    		]
	}
	
	2) input data -  
		 {
        	"title": "Post Test_User again",
    	}
	
	response - status code 400,
		{
    		"content": [
        		"Обязательное поле."
    		]
	}

6) /api/v1/posts/<int:post_id>

	Add and delete a post to the user's subscriptions feed. Method - GET, DELETE
	Only for authorized users
	(Request headers must contain header «Authorizathion»: «Token ...»), if it's missing - error 403
	Input data - None
	
	1) method GET

		1) /api/v1/posts/15

		response - status code 200,	
		{
    		"message": "Post Post User 2 was added to your's subscriptions!!"
		}
	
		response - status code 400,
		{
    		"message": "You are already subscribed to this post!!"
		}	
	
		2) /api/v1/posts/289

		response - status code 404,
		{
    		"message": "Post matching query does not exist."
		}
	
	2) метод DELETE

		1) /api/v1/posts/250

		response - status code 404,
		{
    		"message": "Subscriptions matching query does not exist."
		}
	
		2) /api/v1/posts/15

		response - status code 200,
		{
    		"message": "Post Post User 2 was deleted from your's subscriptions!!"
		}


7) /api/v1/subs

	Method - GET
	View the feed of the user's subscriptions, sorting by the date the post was created
	Pagination - 10 posts per page
	Filtering by post read
	Only for authorized users
	Request headers must contain header «Authorizathion»: «Token ...»), if it's missing - error 403
	Input data - None
	
	1) api/v1/subs
	response - status code 200, 
	{
    "count": 25,   - total quantity of subscriptions
    "next": http://127.0.0.1:8000/api/v1/subs?page=2, - next page on pagination
    "previous": http://127.0.0.1:8000/api/v1/subs, - previos page on pagination
    "results": [
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
        },
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
        },
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
        },
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
        },
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
        },
        .......
    ]
}

	2) /api/v1/subs?readed=True
	
	response - status code 200,
	{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
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
        }
    ]
}


8) /api/v1/subs/<int:sub_id>

	Method - GET, PUT
	GET - View subscription and post in subscription
	PUT -  Make a read mark of post
	Only for authorized users
	Request headers must contain header «Authorizathion»: «Token ...»), if it's missing - error 403
	Input data - None
	
	1) method GET
	
		1) /api/v1/subs/168
	
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
		}
	
		2) /api/v1/subs/261
	
		{
    			"detail": "Страница не найдена."
		}
	
	2) method PUT
	
		1) /api/v1/subs/261
	
		{
    			"detail": "Страница не найдена."
		}
	
		2) /api/v1/subs/168
	
		input data - 
		{
  		"post": {
    			"title": "string",
   	 		"content": "string"
  		},
  		"readed": true
		}
	
		- Post data is read-only and cannot be changed.
	
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
	
	
				
		 
