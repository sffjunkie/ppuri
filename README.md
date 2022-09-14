# ppURI

A [pyparsing](https://pyparsing-docs.readthedocs.io/en/latest/) based URI parser/scanner.

Install using pipx, pip or your tool of choice e.g.

```
pipx install ppuri
```

## Usage

### Parsing

Either import `Uri` from `ppuri.uri` and use the pyparsing `parse_string` method to match and parse against all URI schemes e.g.

```python
from ppuri.uri import Uri
info = Uri.parse_string("https://www.example.com:443/a.path?q=aparam#afragment")
print(inf["scheme"])
print(info["authority"]["address"])
```

prints

```
https
www.example.com
```

Or import a specific scheme

```python
from ppuri.scheme.http import Http
info = Http.parse_string()
```

and use that to parse

### Scanning

To scan text for URIs use the `scan_string` method

## Supported schemes

Currently supports the following schemes

- http(s)
- urn
- aaa
- about
- coap
- crid
- data
- file
- mailto

### Http(s)

`parse_string` returns a dictionary of the form

```python
{
    "scheme": "http" or "https",
    "authority": {
        "address": "hostname" or "ipv4 address" or "ipv6 address",
        "port": "port number",
        "username": "user name if provided",
        "password": "pasword if provided"
    },
    "path": "path if provided",
    "parameters": [
        "list of parameters if provided",
        {
            "name": "parameter name",
            "value": "parameter value or None if not provided"
        }
    ],
    "fragment": "fragment if provided"
}
```

### Urn

`parse_string` returns a dictionary of the form

```python
{
    "scheme": "urn",
    "nid": "Namespace Identifier",
    "nss": "Namespace Specific String"
}
```

### MailTo

`parse_string` returns a dictionary of the form

```python
{
    "scheme": "mailto",
    "addresses": [
        "List of email addresses",
    ]
    "parameters": [
        "list of parameters if provided",
        {
            "name": "bcc",
            "value": "dave@example.com"
        }
}
```

### Data

`parse_string` returns a dictionary of the form

```python
{
    "scheme": "data",
    "type": "Mime type",
    "subtype": "Mime Subtype",
    "encoding": "base64 if specified",
    "data": "The actual data"
}
```

### File

`parse_string` returns a dictionary of the form

```python
{
    "scheme": "file",
    "path": "The /file/path",
}
```