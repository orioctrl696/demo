# Java Demo Application

Small Maven application used to exercise the repository's pull request build,
test, artifact, and security workflows.

## Run locally

```text
mvn test
mvn package
java -jar target/demo-application-1.0.0.jar Java
```

The Terraform workflows are separate and are not required for this application
build.