# ulauncher-kv

Ulauncher extension for set and get snippets of any text in a local database

<p align="center">
  <a href="https://gitter.im/ulauncher-kv/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge"><img src="https://badges.gitter.im/ulauncher-kv/community.svg" alt="Gitter"/></a>
</p>

![kv](kv.gif)

# Requirements

## Technical:
* [ulauncher](https://ulauncher.io/)
* Python >= 2.7

Other:
* [xdotool](https://www.semicomplete.com/projects/xdotool/) -- If you are interested in using the funcionality that paste value directly in the current app (ALT + ENTER shortcut)
```
sudo apt install xdotool
```

# Install

Open ulauncher preferences window -> extensions -> add extension and paste the following url:

```
https://github.com/laercioskt/ulauncher-kv
```

# Usage

## Enter a query in the form of 

```
[set] <key> <value> | [get] <key> [unset] | <key> (simple way to [get])
```

### Example of store a new "key" -> "value"

```
kv set someKey some value
```

### Example of remove a "key" -> "value"

```
kv get someKey unset
```

### Examples of get "value" filtering by "key"

```
kv get someKey

kv get partofakey

kv someKey

kv partofakey
```


# Shortcuts

### To copy selected value to transfer area
```
ENTER
```

### To copy value of a specif position to transfer area
```
ALT + N (where N is the position of a value at the list)
```

### To copy selected value and paste directly in the current app
```
ALT + ENTER: 
```

