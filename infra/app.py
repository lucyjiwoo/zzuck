import aws_cdk as cdk

from stacks.core_infra_stack import ZzuckStack

app = cdk.App()

ZzuckStack(app, "ZzuckStack")

app.synth()
