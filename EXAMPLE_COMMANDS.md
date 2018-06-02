# Example commands used in dockJob

Note: Command output must be utf-8 or an error will occur.

## Get the contents of a webpge

```
wget www.google.com -O- | iconv -f ISO-8859-1 -t UTF-8
```

