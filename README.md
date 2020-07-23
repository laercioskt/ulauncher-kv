# ulauncher-kv

Ulauncher extension for set and get snippets of any text in a local database

![kv](kv.gif)

# Install

Open ulauncher preferences window -> extensions -> add extension and paste the following url:

```
https://github.com/laercioskt/ulauncher-kv
```

# Usage

Enter a query in the form of 

```
[set] <key> <value> | [get] <key> [unset]
```


## example of store a new "key" -> "value"

```
kv set someKey someValue
```

## example of remove a "key" -> "value"

```
kv get someKey unset
```

## examples of get "value" filtering by key

```
kv get someKey
```

```
kv get omeKe
```
