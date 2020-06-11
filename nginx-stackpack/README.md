# StackState Nginx StackPack

This repository contains the StackState Nginx StackPack.

## Introduction

The Nginx StackPack configures StackState to process data produced by the Nginx Topo Agent Check and the Nginx Metrics Agent Check. All this integration can be found in this repository.


## Building

The Nginx StackPack is built using the [SBT](https://www.scala-sbt.org/) tool.

In the main directory, compile the Nginx StackPack using:

```
sbt compile
```

## Testing

The Nginx StackPack comes with a small testing library that validates that the Nginx StackPack packaging is correct.

In the main directory, test the Nginx StackPack using:

```
sbt test
```

## Packaging

In the main directory, package the Nginx StackPack using:

```
sbt package
```

## Versioning

The Nginx StackPack release version is configured in the [version.sbt](version.sbt) file. StackPacks use [Semantic Versioning](https://semver.org/).
