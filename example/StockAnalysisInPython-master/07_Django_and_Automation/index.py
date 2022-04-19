{% load static %}
<html>
    <head>
        <title>This is title.</title>
        <link rel="stylesheet" href={% static "index/style.css" %} /> 
    </head>
    <body>
        <h1>This is heading1 text.</h1>
        <h2>This is heading2 text.</h2>
        <h3>This is heading3 text.</h3>
        <p>This is a paragraph.</p>
        This is plain text.<br /> 
        <b>This is bold text.</b><br />
        <i>This is Italic text.</i><br />
        <s>This is strike text.</s><br />
        <ol>
            <li>the first orderd list</li>
            <li>the second orderd list</li>
            <li>the third orderd list</li>
        </ol>
        <ul>
            <li>unorderd list</li>
            <li>unorderd list</li>
            <li>unorderd list</li>
        </ul>
        <table border=1>
            <tr>
                <th>table header 1</th>
                <th>table header 2</th>
                <th>table header 3</th>
            </tr>
            <tr>
                <td>table data 4</td>
                <td>table data 5</td>
                <td>table data 6</td>
            </tr>
            <tr>
                <td>table data 7</td>
                <td>table data 8</td>
                <td>table data 9</td>
            </tr>
        </table><br />
        <a href="www.djangoproject.com">Visit Django homepage!<br />
        <img src={% static "index/Django_Logo.jpg" %}/></a>
    </body>
</html>