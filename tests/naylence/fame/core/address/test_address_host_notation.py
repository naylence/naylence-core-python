#!/usr/bin/env python3
"""
Test the enhanced FAME address format supporting host-like notation.

Tests both backward compatibility with existing path-only addresses and
new functionality for host-only and host+path combinations.
"""

import pytest

from naylence.fame.core.address.address import (
    FameAddress,
    format_address,
    format_address_from_components,
    parse_address,
    parse_address_components,
    make_fame_address,
)


class TestAddressHostNotation:
    """Test host notation support in FAME addresses."""

    def test_traditional_path_only_addresses(self):
        """Test backward compatibility with existing path-only addresses."""
        # Test parsing traditional addresses
        participant, location = parse_address("alice@/")
        assert participant == "alice"
        assert location == "/"

        participant, location = parse_address("worker@/api/v1/service")
        assert participant == "worker"
        assert location == "/api/v1/service"

        # Test component parsing
        participant, host, path = parse_address_components("alice@/")
        assert participant == "alice"
        assert host is None
        assert path == "/"

        participant, host, path = parse_address_components("worker@/api/v1/service")
        assert participant == "worker"
        assert host is None
        assert path == "/api/v1/service"

    def test_host_only_addresses(self):
        """Test new host-only address format."""
        # Test parsing host-only addresses
        participant, location = parse_address("alice@fame.fabric")
        assert participant == "alice"
        assert location == "fame.fabric"

        participant, location = parse_address("worker@child.fame.fabric")
        assert participant == "worker"
        assert location == "child.fame.fabric"

        # Test component parsing
        participant, host, path = parse_address_components("alice@fame.fabric")
        assert participant == "alice"
        assert host == "fame.fabric"
        assert path is None

        participant, host, path = parse_address_components("worker@child.fame.fabric")
        assert participant == "worker"
        assert host == "child.fame.fabric"
        assert path is None

    def test_host_with_path_addresses(self):
        """Test new host+path address format."""
        # Test parsing host+path addresses
        participant, location = parse_address("alice@fame.fabric/api")
        assert participant == "alice"
        assert location == "fame.fabric/api"

        participant, location = parse_address("worker@child.fame.fabric/service/v1")
        assert participant == "worker"
        assert location == "child.fame.fabric/service/v1"

        # Test component parsing
        participant, host, path = parse_address_components("alice@fame.fabric/api")
        assert participant == "alice"
        assert host == "fame.fabric"
        assert path == "/api"

        participant, host, path = parse_address_components(
            "worker@child.fame.fabric/service/v1"
        )
        assert participant == "worker"
        assert host == "child.fame.fabric"
        assert path == "/service/v1"

    def test_format_address_backward_compatibility(self):
        """Test that format_address works with existing path-only usage."""
        addr = format_address("alice", "/")
        assert str(addr) == "alice@/"

        addr = format_address("worker", "/api/v1")
        assert str(addr) == "worker@/api/v1"

    def test_format_address_host_notation(self):
        """Test format_address with new host notation."""
        # Host-only
        addr = format_address("alice", "fame.fabric")
        assert str(addr) == "alice@fame.fabric"

        # Host+path
        addr = format_address("alice", "fame.fabric/api")
        assert str(addr) == "alice@fame.fabric/api"

    def test_format_address_from_components(self):
        """Test creating addresses from separate components."""
        # Path only
        addr = format_address_from_components("alice", path="/")
        assert str(addr) == "alice@/"

        addr = format_address_from_components("worker", path="/api/v1")
        assert str(addr) == "worker@/api/v1"

        # Host only
        addr = format_address_from_components("alice", host="fame.fabric")
        assert str(addr) == "alice@fame.fabric"

        addr = format_address_from_components("worker", host="child.fame.fabric")
        assert str(addr) == "worker@child.fame.fabric"

        # Host + path
        addr = format_address_from_components("alice", host="fame.fabric", path="/api")
        assert str(addr) == "alice@fame.fabric/api"

        addr = format_address_from_components(
            "worker", host="child.fame.fabric", path="/service/v1"
        )
        assert str(addr) == "worker@child.fame.fabric/service/v1"

    def test_make_fame_address_all_formats(self):
        """Test make_fame_address with all supported formats."""
        # Path only
        addr = make_fame_address("alice@/")
        assert isinstance(addr, FameAddress)
        assert str(addr) == "alice@/"

        # Host only
        addr = make_fame_address("alice@fame.fabric")
        assert isinstance(addr, FameAddress)
        assert str(addr) == "alice@fame.fabric"

        # Host + path
        addr = make_fame_address("alice@fame.fabric/api")
        assert isinstance(addr, FameAddress)
        assert str(addr) == "alice@fame.fabric/api"

    def test_address_validation_errors(self):
        """Test that invalid addresses raise appropriate errors."""
        # Empty location
        with pytest.raises(ValueError, match="Location part cannot be empty"):
            parse_address("alice@")

        # Missing @
        with pytest.raises(ValueError, match="Missing '@'"):
            parse_address("alice")

        # Invalid participant
        with pytest.raises(ValueError, match="Participant must match"):
            parse_address("alice!@/")

        # Invalid host segment
        with pytest.raises(ValueError, match="Bad host segment"):
            parse_address("alice@bad!host")

        # Invalid path segment
        with pytest.raises(ValueError, match="Bad segment"):
            parse_address("alice@/bad!path")

        # Empty host segment
        with pytest.raises(ValueError, match="Empty host segment"):
            parse_address("alice@host..name")

    def test_format_address_from_components_validation(self):
        """Test validation in format_address_from_components."""
        # Must provide at least one of host or path
        with pytest.raises(
            ValueError, match="At least one of host or path must be provided"
        ):
            format_address_from_components("alice")

    def test_wildcards_no_longer_supported_in_physical_addresses(self):
        """Test that wildcards are no longer supported in physical addresses."""
        # Wildcards should fail in physical addresses
        with pytest.raises(ValueError, match="not allowed"):
            parse_address_components("alice@/api/*")

        with pytest.raises(ValueError, match="Bad segment"):
            parse_address_components("alice@/api/**")

        with pytest.raises(ValueError, match="not allowed"):
            parse_address_components("alice@fame.fabric/api/*")

    def test_complex_host_names(self):
        """Test various valid host name formats."""
        valid_hosts = [
            "fame.fabric",
            "child.fame.fabric",
            "deep.child.fame.fabric",
            "node-1.cluster.fame.fabric",
            "127.0.0.1",  # IP-like (allowed by validation)
            "single",  # Single segment
        ]

        for host in valid_hosts:
            participant, parsed_host, path = parse_address_components(f"alice@{host}")
            assert participant == "alice"
            assert parsed_host == host
            assert path is None

    def test_roundtrip_parsing_and_formatting(self):
        """Test that parsing and formatting are consistent."""
        test_addresses = [
            "alice@/",
            "worker@/api/v1/service",
            "alice@fame.fabric",
            "worker@child.fame.fabric",
            "alice@fame.fabric/api",
            "worker@child.fame.fabric/service/v1/endpoint",
            "service@node-1.cluster.fame.fabric/health",
        ]

        for addr_str in test_addresses:
            # Parse and reformat should give same result
            participant, location = parse_address(addr_str)
            recreated = format_address(participant, location)
            assert str(recreated) == addr_str

            # Component parsing and formatting should also work
            participant, host, path = parse_address_components(addr_str)
            if host and path:
                recreated = format_address_from_components(
                    participant, host=host, path=path
                )
            elif host:
                recreated = format_address_from_components(participant, host=host)
            else:
                recreated = format_address_from_components(participant, path=path)
            assert str(recreated) == addr_str


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
