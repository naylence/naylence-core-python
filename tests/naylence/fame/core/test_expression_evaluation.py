#!/usr/bin/env python3
"""
Example demonstrating expression evaluation policies in ResourceConfig.
"""
import os
import json
from naylence.fame.core.util.resource_config import ResourceConfig
from naylence.fame.core.util.expression_policy import ExpressionEvaluationPolicy


class JwtAuthorizer(ResourceConfig):
    """Example JWT authorizer configuration."""

    type: str = "JwtAuthorizer"
    issuer: str
    audience: str
    required_scopes: str


def main():
    # Set up environment variables for testing
    os.environ["AUTH_ISSUER"] = "https://auth.prod.example.com"
    os.environ["AUTH_AUD"] = "naylence-production"
    # Note: AUTH_SCOPES is not set, so default will be used

    # Example configuration with expressions
    config_data = {
        "type": "JwtAuthorizer",
        "issuer": "${env:AUTH_ISSUER:https://auth.dev.local}",
        "audience": "${env:AUTH_AUD:naylence-node}",
        "required_scopes": "${env:AUTH_SCOPES:fabric.read fabric.write}",
    }

    print("Original config data:")
    print(json.dumps(config_data, indent=2))
    print()

    # Test EVALUATE policy (default)
    print("=== EVALUATE policy (default) ===")
    config = ResourceConfig.model_validate(config_data)
    print(f"Type: {type(config)}")
    print(f"Issuer: {config.issuer}")
    print(f"Audience: {config.audience}")
    print(f"Required scopes: {config.required_scopes}")
    print()

    # Test LITERAL policy
    print("=== LITERAL policy ===")
    config_literal = ResourceConfig.model_validate(
        config_data,
        context={"expression_evaluation_policy": ExpressionEvaluationPolicy.LITERAL},
    )
    print(f"Type: {type(config_literal)}")
    print(f"Issuer: {config_literal.issuer}")
    print(f"Audience: {config_literal.audience}")
    print(f"Required scopes: {config_literal.required_scopes}")
    print()

    # Test ERROR policy
    print("=== ERROR policy ===")
    try:
        ResourceConfig.model_validate(
            config_data,
            context={"expression_evaluation_policy": ExpressionEvaluationPolicy.ERROR},
        )
        print("ERROR: Should have raised an exception!")
    except Exception as e:
        print(f"Expected error: {e}")
    print()

    # Test backward compatibility with old disable flag
    print("=== Backward compatibility (disable_expression_evaluation) ===")
    config_compat = ResourceConfig.model_validate(
        config_data, context={"disable_expression_evaluation": True}
    )
    print(f"Type: {type(config_compat)}")
    print(f"Issuer: {config_compat.issuer}")
    print(f"Audience: {config_compat.audience}")
    print(f"Required scopes: {config_compat.required_scopes}")
    print()

    # Test string policy values
    print("=== String policy values ===")
    config_str_literal = ResourceConfig.model_validate(
        config_data, context={"expression_evaluation_policy": "literal"}
    )
    print(f"String 'literal' policy - Issuer: {config_str_literal.issuer}")
    print()

    # Serialization test
    print("=== Serialization test ===")
    serialized = config.model_dump()
    print("Serialized config:")
    print(json.dumps(serialized, indent=2))


if __name__ == "__main__":
    main()
