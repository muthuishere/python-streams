# python-functional-stream
Streams in Python for concise code

```python
#Instead of writing like this
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

list(map(lambda user: user['first_name'],  filter(lambda user:user['salary'] > 80000, filter(lambda product: product['gender'] == 'Male',users))))

#Write this
from streams.Stream import Stream

results = (Stream
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

```

