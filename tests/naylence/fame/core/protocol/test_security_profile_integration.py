"""
Test SecuritySettings integration with frames.
"""

import pytest
from naylence.fame.core.protocol.frames import NodeHelloFrame, NodeWelcomeFrame
from naylence.fame.core import SecuritySettings, SigningMaterial


class TestSecuritySettingsIntegration:
    """Test cases for SecuritySettings integration with protocol frames."""

    def test_node_hello_frame_with_security_settings(self):
        """Test NodeHelloFrame with explicit SecuritySettings."""
        hello_with_profile = NodeHelloFrame(
            system_id="test-node-123",
            instance_id="instance-456",
            security_settings=SecuritySettings(
                signing_material=SigningMaterial.X509_CHAIN
            ),
        )

        assert hello_with_profile.security_settings is not None
        assert (
            hello_with_profile.security_settings.signing_material
            == SigningMaterial.X509_CHAIN
        )

    def test_node_hello_frame_without_security_settings(self):
        """Test NodeHelloFrame without explicit SecuritySettings (should be None)."""
        hello_without_profile = NodeHelloFrame(
            system_id="test-node-789", instance_id="instance-012"
        )

        assert hello_without_profile.security_settings is None

    def test_json_serialization_round_trip(self):
        """Test JSON serialization and deserialization of frames with SecuritySettings."""
        hello_with_profile = NodeHelloFrame(
            system_id="test-node-123",
            instance_id="instance-456",
            security_settings=SecuritySettings(
                signing_material=SigningMaterial.X509_CHAIN
            ),
        )

        # Serialize to JSON
        hello_json = hello_with_profile.model_dump(by_alias=True)
        assert isinstance(hello_json, dict)

        # Deserialize from JSON
        hello_restored = NodeHelloFrame.model_validate(hello_json)
        assert hello_restored.security_settings is not None
        assert (
            hello_restored.security_settings.signing_material
            == SigningMaterial.X509_CHAIN
        )
        assert hello_restored.system_id == "test-node-123"
        assert hello_restored.instance_id == "instance-456"

    def test_node_welcome_frame_with_security_settings(self):
        """Test NodeWelcomeFrame with SecuritySettings."""
        welcome = NodeWelcomeFrame(
            system_id="assigned-node-456",
            instance_id="instance-456",
            security_settings=SecuritySettings(
                signing_material=SigningMaterial.X509_CHAIN
            ),
        )

        assert welcome.security_settings is not None
        assert welcome.security_settings.signing_material == SigningMaterial.X509_CHAIN

    def test_backward_compatibility_old_json(self):
        """Test backward compatibility with old JSON without security_settings."""
        old_hello_json = {
            "type": "NodeHello",
            "systemId": "old-node",
            "instanceId": "old-instance",
        }

        old_hello = NodeHelloFrame.model_validate(old_hello_json)
        assert old_hello.security_settings is None  # Should be None if not provided
        assert old_hello.system_id == "old-node"
        assert old_hello.instance_id == "old-instance"

    def test_security_settings_serialization(self):
        """Test SecuritySettings serialization details."""
        profile = SecuritySettings(signing_material=SigningMaterial.X509_CHAIN)
        profile_dict = profile.model_dump(by_alias=True)

        assert isinstance(profile_dict, dict)

        # Test round-trip
        restored_profile = SecuritySettings.model_validate(profile_dict)
        assert restored_profile.signing_material == SigningMaterial.X509_CHAIN


if __name__ == "__main__":
    pytest.main([__file__])
