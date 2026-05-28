import aws_cdk as cdk

from stacks.zzuck_stack import ZzuckStack

app = cdk.App()

ZzuckStack(app, "ZzuckStack")

app.synth()
