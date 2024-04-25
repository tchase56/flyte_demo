from flytekit import task, workflow


@task
def say_hello(name: str) -> str:
    return f"Hello, {name}!"


@workflow
def hello_world_wf(name: str = 'world') -> str:
    res = say_hello(name=name)
    return res


if __name__ == "__main__":
    print(f"Running wf() {hello_world_wf(name='passengers')}")