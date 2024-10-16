import datetime

#Working with binary files, going above and beyond.
#We will process removals first, then additions.
@dataClass
class JournalAddition:
    insertionPoint: int
    data: bytes
    
@dataClass
class JournalRemoval:
    removalStart: int
    removalEnd: int


@dataClass
class Commit:
    additions: list[JournalAddition]
    removals: list[JournalRemoval]
    timestamp: datetime


@dataClass
class Journal:
    commits: list[Commit] #This must be ordered. 