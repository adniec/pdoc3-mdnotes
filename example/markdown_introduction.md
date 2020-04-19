Let's walk through basic elements:

# Heading

Write `# Heading` in new line to create first level heading. You can specify level of heading by adding more `#`. Just 
take a look at examples below and how they are presented on the left side (navigation bar).

## Subheading

`## Subheading` 

## Next subheading

`## Next subheading` 

### Deeper subheading

`### Deeper subheading` 

# Text

## paragraph

Separate text with one blank line to make paragraph.

As it is done here.

## separator

`---` to create separator. Like this one below:

---

## italic

Wrap text with `*` to make it italic, e.g. `*I want it italic*` will be displayed as: *I want it italic*.

## bold

Wrap text with `**` to make it bold, e.g. `**I want it bold**` will be displayed as: **I want it bold**.

## both

***Note:** you can mix it in one sentence. Just don't forget to close each asterisk.* 

```markdown
***Note:** you can mix it in one sentence. Just don't forget to close each asterisk.* 
```

# List

Start each line with `number` or `-` to make a list. If you want to create sublist add indentation. Stick with it for 
each subpoint. You can mix ordered lists with unordered like on example below:

- One
- Two
    1. one
    2. two
        1. One and one
        2. One and two
- Three
    - sub three
        - sub sub three


# Link

To add link write text that you like to display in brackets and place (address) just after it. As on following example:
```
[homepage](https://ethru.github.io/pdoc3-mdnotes/)
```
It will transform into: [homepage](https://ethru.github.io/pdoc3-mdnotes/).

# Image

![Logo](https://raw.githubusercontent.com/ethru/pdoc3-mdnotes/master/pdoc3_mdnotes/icons/mdnotes.png)

Rules with image are quite the same as with link. One exception is that you need to place `!` before brackets. Example:
```
![Logo](https://raw.githubusercontent.com/ethru/pdoc3-mdnotes/master/pdoc3_mdnotes/icons/mdnotes.png)
```
You can place alternate text displayed when image couldn't be loaded in brackets or leave them empty `[]`. Then broken 
link will look like:
![](https://github.com/ethru/NOimg.jpg)

# More

Pure basics were presented here. I strongly encourage you to experiment with those and [further read
](https://www.markdownguide.org/).
