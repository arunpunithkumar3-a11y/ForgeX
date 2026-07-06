from dataclasses import dataclass

@dataclass(frozen=True)
class Environment:
    name: str
    docker_image: str


ENVIRONMENT_REGISTRY: dict[str, Environment] = {
    "python": Environment(name="python", docker_image="python:3.12-slim"),
    "javascript": Environment(name="javascript", docker_image="node:22"),
    "typescript": Environment(name="typescript", docker_image="node:22"),
    "java": Environment(name="java", docker_image="eclipse-temurin:21"),
    "c": Environment(name="c", docker_image="gcc:14"),
    "cpp": Environment(name="cpp", docker_image="gcc:14"),
    "go": Environment(name="go", docker_image="golang:1.24"),
    "rust": Environment(name="rust", docker_image="rust:1.89"),
    "csharp": Environment(name="csharp", docker_image="mcr.microsoft.com/dotnet/sdk:9.0"),
    "php": Environment(name="php", docker_image="php:8.4-cli"),
    "ruby": Environment(name="ruby", docker_image="ruby:3.4"),
    "kotlin": Environment(name="kotlin", docker_image="gradle:8.14-jdk21"),
    "swift": Environment(name="swift", docker_image="swift:6.1"),
    "dart": Environment(name="dart", docker_image="dart:stable"),
    "scala": Environment(name="scala", docker_image="sbtscala/scala-sbt:eclipse-temurin-21.0.8_9_1.11.4_3.7.3"),
    "r": Environment(name="r", docker_image="r-base:4.5.1"),
    "lua": Environment(name="lua", docker_image="nickblah/lua:5.4"),
    "perl": Environment(name="perl", docker_image="perl:5.42"),
    "elixir": Environment(name="elixir", docker_image="elixir:1.18"),
    "haskell": Environment(name="haskell", docker_image="haskell:9.12"),
}


def get_image(language: str) -> str:
    env = ENVIRONMENT_REGISTRY.get(language.lower())
    return env.docker_image if env else "Image not found"

if __name__ =="__main__":
    print(get_image("python"))
    print(get_image("javascript"))
    print(get_image("java"))
    print(get_image("c"))
    print(get_image("cpp"))
    print(get_image("go"))
    print(get_image("rust"))
    print(get_image("csharp"))
    print(get_image("php"))
    print(get_image("ruby"))
    print(get_image("kotlin"))
    print(get_image("swift"))
    print(get_image("dart"))
    print(get_image("scala"))
    print(get_image("r"))
    print(get_image("lua"))
    print(get_image("perl"))
    print(get_image("elixir"))
    print(get_image("haskell"))