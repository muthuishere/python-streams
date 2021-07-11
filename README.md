# functional-streams
Writing concise functional code in python

![Converting to concise code](https://github.com/muthuishere/python-streams/blob/main/assets/pythonstreams.png?raw=true)


<a target="_blank" href="https://www.youtube.com/watch?v=AcQcxh0VQv0">Demo </a>


```python

#To Fetch from a list of users
#       Get their firstname , if their salary greater than 80000 and gender is male

#Instead of writing like this


list(map(lambda user: user['first_name'],  
         filter(lambda user:user['salary'] > 80000, 
                filter(lambda product: product['gender'] == 'Male',
                       users))))

#Write this
from streams.Stream import Stream

(Stream
   .create(users)
   .filter(lambda user:user['salary'] > 80000)
   .filter(lambda product: product['gender'] == 'Male')
   .map(lambda user: user['first_name'])
   .asList())

#A concise way to write lambdas,functional code in python

```

```python
from streams.Stream import Stream
users = [
    {
        "id": 1,
        "first_name": "Mandy",
        "last_name": "Gowan",
        "email": "mgowan0@aol.com",
        "gender": "Female",
        "loves": ['Soccer','Cricket','Golf'],
        "salary": 119885
    },
    {
        "id": 2,
        "first_name": "Janessa",
        "last_name": "Cotterell",
        "email": "jcotterell1@aol.com",
        "gender": "Female",
        "loves": ['Cricket'],
        "salary": 107629
    },
    {
        "id": 6,
        "first_name": "Jasen",
        "last_name": "Franzini",
        "email": "jfranzini5@aol.com",
        "gender": "Male",
        "loves": ['Soccer','Golf'],
        "salary": 78373
    }
]

#Using Map Filter 
results = (Stream
           .create(users)
           .filter(lambda user:user['salary'] > 80000)
           .map(lambda user: user['first_name'])
           .asList())
#['Mandy', 'Janessa']


#Using Reduce


#Using flatMap Distinct 
results = (Stream
           .create(users)
           .flatmap(lambda user:user['loves'] )
           .distinct()
           .asList())
#['Cricket', 'Golf', 'Soccer']

#Using skip take 
results = (Stream
           .create(users)
           .skip(1)
           .take(1)
           .map(lambda user: user['first_name'])
           .asList())
#['Janessa']


#Even you can peek results
results = (Stream
           .create(users)
            .filter(lambda user:user['gender'] == 'Female')
           .peek(lambda data:print("User",data))
           .map(lambda user: user['first_name'])
           .asList())
#Will list out all female users and print 

#To Reduce
sum_of_female_salaries = (Stream
                   .create(users)
                   .filter(lambda user: user['gender'] == 'Female')
                    .map(lambda user:user['salary'])
                   .reduce(operator.add)
                   .asSingle())

#Will print sum of female user salaries
#227514
```

## Additional Information
#### Design
Most of the functions underneath uses the same functions available in python (map uses map , filter uses filter etc..).
Only we have added wrapper to make the code concise


#### Abstractions
If you need to use abstract items, use the same chaining and just invoke the stream when you are using it
        as the generators used get corrupted by the very first expansion
For Example

```python


stream_of_users = (Stream
                    .create(users)
                    )

#The below code might not work , as the genrators expire once you aggregate it
total_users = (stream_of_users
               .length())

firstname_of_users = (stream_of_users           
                           .map(lambda user: user['first_name'])
                           .asList())


#The above code should be rewritten as
total_users = (stream_of_users
                .stream()
                .length())

firstname_of_users = (stream_of_users
                           .stream()
                           .map(lambda user: user['first_name'])
                           .asList())

# The stream will make use of copying the generators



```

#### Transducers
If you need to use transducers, create with Stream.compose and connect with pipe whenever required

For Example

```python

skip_five_and_take_three_items = (Stream
                                          .compose()
                                          .skip(5)
                                          .take(3)
                                          )

skip_five_and_take_three_items_within_zero_to_hundred = (Stream
                                                         .create(range(100))
                                                         .pipe(skip_five_and_take_three_items)
                                                         .asList()
                                                         )
# Result [5, 6, 7]


skip_five_and_take_three_items_within_zero_to_hundred_and_get_one = (Stream
                                                                 .create(range(100))
                                                                 .pipe(skip_five_and_take_three_items)
                                                                 .take(1)
                                                                 .asList()
                                                                 )
# Result [5]


#To Execute Transducers with Aggregate functions
sum_of_salaries_function = (Stream
                           .compose()
                           .filter(lambda user: user['gender'] == 'Male')
                           .map(lambda user: user['salary'])
                           .reduce(operator.add)
                           )
sum_of_salaries = (Stream
                   .create(get_users())
                   .pipe(sum_of_salaries_function)
                   .asSingle()
                   )
#Result 977023
        
        


```
