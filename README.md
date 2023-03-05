# Bash Memo

Bookmark commands for later reuse. Command will be stored in the cloud.
Like that if you change your laptop. You will be able to get them back.
Our mantra is "Type a command only once!"

Install me

```
pip install git+https://github.com/blancheta/bashmemo.git#egg=bashmemo
```

### How to use it?

Pre-requisites
```
export HISTSIZE=1000000000
export SAVEHIST=$HISTSIZE
setopt EXTENDED_HISTORY
```

Bookmark a command for further use in your career
```
bm -b "your command"
Any keywords to find back this command? (separated by empty space): aws list
```

Search for a bookmarked command
```
Ctrl + S
bm-i-search: <here you can type keywords, or part of the command>
Enter
aws s3 ls (ordered by usage)
aws s2 blabla
aws ec2 blalblalblalbla
You can use tab to select the command your are interested in and then enter
```

Automatic bookmarking based on your bash history
```
bm -ad --autodiscover
```


