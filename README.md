# Robot Framework Remote Resource Allocator

Resource locking library for Robot Framework.

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

# Remote server

Library provide command line util `robot_lockable` that provide robot remote 
server for lockable functionality. 
This is useful when resources located remotely 
for test case.

```
robot_lockable --help
Usage: robot_lockable [OPTIONS]

  main function for remote plugin

Options:
  --port INTEGER              RemoteLockable server Port
  --host TEXT                 Interface to listen. Use "0.0.0.0" to get access
                              from external machines

  --hostname TEXT             Hostname
  --resources_list_file TEXT  Resources list file
  --lock_folder TEXT          Lock folder
  --doc TEXT                  generate documentation. E.g. doc.html or list
  --help                      Show this message and exit.
```

# Run Remote Server In Docker Container

Docker container is run using command below. Replace path to resource.json and hostname with project specific values:

    docker run \
      -p 8270:8270 \
      -v <local path to the resource.json folder>:/<path to resource.json folder> \
      --hostname $(hostname) \
      jussiva/robot-lockable:latest \
      --resources_list_file <path to resource.json folder>

## Full example

To run example resource allocator located in this repository, docker run command is:

    docker run \
      -p 8270:8270 \
      -v $PWD/example:/example/ \
      --hostname hostname \
      --rm \
      jussiva/robot-lockable:latest \
      --resources_list_file /example/resource.json
