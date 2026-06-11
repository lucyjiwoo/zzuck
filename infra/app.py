import aws_cdk as cdk

from stacks.core_infra_stack import CareerIQStack

app = cdk.App()

CareerIQStack(app, "CareerIQStack")

app.synth()
