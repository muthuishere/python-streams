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
from streams.operations.operators import item

(Stream
   .create(users)
   .filter(item['salary'] > 80000)
   .filter(item['gender'] == 'Female')
   .map(item['first_name'])
   .asList())


# You could have seen there is no lambdas involved in above code, 
#      I havent missed it , the implementation & dynamism of python does wraps it.
# You are free to use lambdas or functions as well , something like below


(Stream
   .create(users)
   .filter(lambda user:user['salary'] > 80000)
   .filter(lambda product: product['gender'] == 'Male')
   .map(lambda user: user['first_name'])
   .asList())


#A concise way to write functional code in python

```

```python
from streams.Stream import Stream
from streams.operations.operators import item
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
           .filter(item['salary'] > 80000)
           .map(item['first_name'])
           .asList())
#['Mandy', 'Janessa']

#Using flatMap Distinct 
results = (Stream
           .create(users)
           .flatmap(item['loves'] )
           .distinct()
           .asList())
#['Cricket', 'Golf', 'Soccer']

#Using skip take 
results = (Stream
           .create(users)
           .skip(1)
           .take(1)
           .map(item['first_name'])
           .asList())
#['Janessa']


#Even you can peek results
results = (Stream
           .create(users)
           .peek(lambda data:print("User",data))
           .map(item['first_name'])
           .asList())

#also for peek with item.print or can use side effects inside
(Stream
   .create(users)
   .peek(item.print)
   .map(item['first_name'])
   .asList())

#Will list out all users

```

```text
babynames.csv

Id,Male name,Female name
1,Liam,Olivia
2,Noah,Emma
```


```python
#From CSV to csv
from streams.FileStream import FileStream
from streams.operations.operators import item

(FileStream.createFromCsv(full_path_of_input_csv)
         .filter(item['Female name'].startswith("A"))
         .map(item['Female name'])
         .peek(item.print)
         .asCSV(full_path_of_output_csv))

```

```python
#From text and to text
from streams.FileStream import FileStream


(FileStream.createFromText(full_path_of_input_text)
         .filter(lambda value: value.startswith("A"))
         .peek(lambda val: print(val))         
         .asTextFile(full_path_of_output_text))

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

from streams.Stream import Stream
from streams.operations.operators import item

stream_of_users = (Stream
                   .create(users)
                   )

# The below code might not work , as the genrators expire once you aggregate it
total_users = (stream_of_users
               .length())

firstname_of_users = (stream_of_users
                      .map(lambda user: user['first_name'])
                      .asList())

# The above code should be rewritten as
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
If you need to use transducers, create with Stream.transducer and connect with pipe whenever required

For Example

```python

skip_five_and_take_three_items = (Stream
                                  .transducer()
                                  .skip(5)
                                  .take(3)
                                  )

skip_five_and_take_three_items_within_zero_to_hundred = (Stream
                                                         .createFromText(range(100))
                                                         .pipe(skip_five_and_take_three_items)
                                                         .asList()
                                                         )
# Result [5, 6, 7]

skip_five_and_take_three_items_within_700_to_800 = (Stream
                                                    .createFromText(range(700, 800))
                                                    .pipe(skip_five_and_take_three_items)
                                                    .asList()
                                                    )
# Result [705, 706, 707]





```


# Built for Performance 
This is just a syntactic sugar, with no other third party software involved.
Everything has been written with built-in modules, Because of very hard fights with <a href="https://github.com/yawpitch/">yawpitch</a>. I started taking it seriously, Thanks for his valuable suggestions.

