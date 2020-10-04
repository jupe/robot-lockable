# robot-lockable

Resource locking module. Provide remote keywords and local keywords.

# Usage
Library import
```
Library     RobotLockable       lock_folder=.   resource_list_file=example/resource.json    (hostname=hostname)
```

Available Keywords

| keyword | arguments | note | 
|---------|----|----|
| `lock` | `<requirements>` (`<timeout_s>`)   | Allocate resource using giving requirements |
| `unlock` | `<resource>` | Release resource |

See more details using Remote library CLI to generate documentation:
`python3 RobotLockable/Remote.py --doc`

