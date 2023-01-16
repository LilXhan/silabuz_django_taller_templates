# silabuz_django_taller_templates
# Taller

Los templates ya los hemos usado desde Flask, pero ¿qué son exactamente?

Un template es una plantilla en la cual podemos reemplazar datos variables, por información que nosotros coloquemos, esto lo podemos tomar como funciones, ya que los parámetros son templates dentro del código de la función.

Por ejemplo, teniendo el siguiente template.

```html
Hola me llamo {{nombre}}.
```

Todo lo colocado en `{{}}`, se tomará como un espacio separado para la información que reciba la plantilla. Justamente con las plantillas podemos tener información dinámica, justamente el tipo de uso que se da actualmente.

## Templates tags

Para recrear los ejemplos haremos uso del siguiente ListView

Con este tipo de vista obtenemos una plantilla que nos permite mostrar múltiples instancias de una tabla de nuestra base de datos.

Por ejemplo, teniendo en base el modelo de `Book`

```py
class Book(models.Model):
    bookID = models.IntegerField(primary_key=True)
    title = models.TextField()
    authors = models.TextField()
    average_rating = models.FloatField()
    isbn = models.CharField(max_length=12)
    isbn13 = models.BigIntegerField()
    language_code = models.CharField(max_length=10)
    num_pages = models.IntegerField()
    ratings_count = models.IntegerField()
    text_reviews_count = models.IntegerField()
    publication_date = models.CharField(max_length=20)
    publisher = models.CharField(max_length=300)
```

Podemos implementar una vista de este tipo:

```py
from django.views.generic.list import ListView
from .models import Book

class BookList(ListView):
    model = Book
    template_name = "booklist.html"
```

Implementamos el template dentro de la ruta `myapp/templates`:

```html
<ul>
    <!-- Iterate over object_list -->
    {% for object in object_list %}
    <!-- Display Objects -->
    <li>{{ object.title }}</li>
    <li>{{ object.authors }}</li>

    <hr/>
    <!-- If object_list is empty  -->
    {% empty %}
    <li>No hay objetos.</li>
    {% endfor %}
</ul>
```

![ListView](https://photos.silabuz.com/uploads/big/6f1af8fd4c2e3093145c0b9913fa1bae.PNG)

La ruta en la que se use, es independiente.

### Cycle

Cycle funciona de la misma que un form, con la diferencia que normalmente se hace uso en base a un iterable, y este tiene valores definidos, que suelen ser muy pocos.

Por ejemplo, modificando nuestro template de la siguiente forma.

```html
<ul>
    <!-- Iterate over object_list -->
    {% for object in object_list %}
    <!-- Display Objects -->
    <div  style='background-color:{% cycle 'lightblue' 'pink' 'yellow' 'coral' 'grey' %}'>
    <li>{{ object.title }}</li>
    <li>{{ object.authors }}</li>
    </div>

    <hr/>
    <!-- If object_list is empty  -->
    {% empty %}
    <li>No objects yet.</li>
    {% endfor %}
</ul>
```

Obtenemos el siguiente resultado.

![Cycle](https://photos.silabuz.com/uploads/big/105be4770df568c626f13bb7c3f0c863.PNG)

### Extends

Extends sirve, como su nombre lo indica para extender un template. Por ejemplo, podemos tener información común entre diversos templates. Por lo que, se puede refactorizar para crear un template general, por lo que podemos usar la misma base para distintas instancias.

Por ejemplo, creamos `base.html`.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <title>Uso de extend</title>
</head>
<body>
    <h1>Uso de extend</h1>
    {% block content %}
    {% endblock %}
</body>
</html>  
```

Con `{% block content %}`, Creamos un espacio donde se va a asignar el contenido del extend.

Modificamos nuestro `booklist.html`.

```html
{% extends 'base.html' %}

{% block content %}
<ul>
    <!-- Iterate over object_list -->
    {% for object in object_list %}
    <!-- Display Objects -->
    <div  style='background-color:{% cycle 'lightblue' 'pink' 'yellow' 'coral' 'grey' %}'>
    <li>{{ object.title }}</li>
    <li>{{ object.authors }}</li>
    </div>

    <hr/>
    <!-- If object_list is empty  -->
    {% empty %}
    <li>No objects yet.</li>
    {% endfor %}
</ul>

{% endblock %}
```

Luego de volver a recargar la página, obtenemos el siguiente resultado.

![Extend](https://photos.silabuz.com/uploads/big/e338b65c5c4885b3d1e46d31041b274c.PNG)

## Filters

Los filtros, funcionan de forma similar que las tuberías de agregación de Mongo, básicamente se encargan de modificar la información en base a lo que se especifique.

### filter

Podemos convertir a letra minúscula o mayúscula.

```html
{% extends 'base.html' %}

{% block content %}
<ul>
    <!-- Iterate over object_list -->
    {% for object in object_list %}
    <!-- Display Objects -->
    <div  style='background-color:{% cycle 'lightblue' 'pink' 'yellow' 'coral' 'grey' %}'>
    {% filter lower %}
    <li>{{ object.title }}</li>
    {% endfilter %}
    <li>{{ object.authors }}</li>
    </div>

    <hr/>
    <!-- If object_list is empty  -->
    {% empty %}
    <li>No objects yet.</li>
    {% endfor %}
</ul>

{% endblock %}
```

### Uso de filters con if

Podemos agregar filtros a condicionales if. Por ejemplo, queremos mostrar los autores con menos de 30 de tamaño.

Añadimos el siguiente condicional para filtrar nuestros resultados.

```html
{% extends 'base.html' %}

{% block content %}
<ul>
    <!-- Iterate over object_list -->
    {% for object in object_list %}
    <!-- Display Objects -->
    <div  style='background-color:{% cycle 'lightblue' 'pink' 'yellow' 'coral' 'grey' %}'>
    {% filter lower %}
    <li>{{ object.title }}</li>
    {% endfilter %}
    {% if object.authors|length <= 30 %}
    <li>{{ object.authors }}</li>
    <li>Tamaño del autor: {{object.authors|length}}</li>
    {% endif %}
    </div>

    <hr/>
    <!-- If object_list is empty  -->
    {% empty %}
    <li>No objects yet.</li>
    {% endfor %}
</ul>

{% endblock %}
```

Vemos que, al volver a ejecutar obtenemos que todos los tamaños son menores de 30.

## Tarea

Modificar la vista actual y añadir los siguientes atributos.

-   `language_code`
    
-   `publisher`
    
-   `text_reviews_count`
    

Luego con los nuevos atributos, filtrar los registros en base a los siguientes datos:

-   `publisher` debe tener un tamaño menor igual a 20
    
-   `text_reviews_count` debe ser mayor 10
    

Luego con la información filtrada, añadir el siguiente tag.

-   Volver en mayúsculas `language_code`

### Consideraciones

Hacer uso de `and` al momento de concatenar el `if` para realizar correctamente el filtrado.


- [Diapositiva](https://docs.google.com/presentation/d/e/2PACX-1vS-iWShuvwvH82B3qQuSQEyum2fNDRM8XzUhK6_voZxHetjWCLFq6Q9_6CJO0PTjZe7uiATtO7lOCl4/embed?start=false&loop=false&delayms=3000)
