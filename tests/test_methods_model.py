# -*- coding: utf-8 -*-

import pytest
import dataclasses
from sanhe_confluence_sdk.methods.model import BaseResponse, NA


# --- Test fixtures: Define nested response models for testing ---
@dataclasses.dataclass(frozen=True)
class Address(BaseResponse):
    @property
    def city(self) -> str:
        return self._get("city")

    @property
    def zip_code(self) -> str:
        return self._get("zip_code")


@dataclasses.dataclass(frozen=True)
class Contact(BaseResponse):
    @property
    def phone(self) -> str:
        return self._get("phone")

    @property
    def email(self) -> str:
        return self._get("email")


@dataclasses.dataclass(frozen=True)
class User(BaseResponse):
    @property
    def name(self) -> str:
        return self._get("name")

    @property
    def contact(self) -> Contact:
        return self._new(Contact, "contact")

    @property
    def addresses(self) -> list[Address]:
        return self._new_many(Address, "addresses")


class TestBaseResponseRawData:
    """Tests for raw_data property."""

    def test_returns_underlying_data(self):
        """raw_data should return the exact dict passed to _raw_data."""
        data = {"name": "Alice", "age": 30}
        response = BaseResponse(_raw_data=data)
        assert response.raw_data == data
        assert response.raw_data is data  # Same object reference

    def test_empty_data(self):
        """raw_data should work with empty dict."""
        response = BaseResponse(_raw_data={})
        assert response.raw_data == {}

    def test_nested_data(self):
        """raw_data should preserve nested structures."""
        data = {"user": {"name": "Bob", "scores": [1, 2, 3]}}
        response = BaseResponse(_raw_data=data)
        assert response.raw_data == data


class TestBaseResponseGet:
    """Tests for _get method."""

    def test_field_exists(self):
        """_get should return field value when field exists."""
        response = BaseResponse(_raw_data={"name": "Alice"})
        assert response._get("name") == "Alice"

    def test_field_not_exists(self):
        """_get should return NA sentinel when field is absent."""
        response = BaseResponse(_raw_data={})
        result = response._get("missing")
        assert result is NA

    def test_field_is_none(self):
        """_get should return None when field value is explicitly None."""
        response = BaseResponse(_raw_data={"value": None})
        assert response._get("value") is None

    def test_field_is_empty_string(self):
        """_get should return empty string (not NA) when value is empty string."""
        response = BaseResponse(_raw_data={"value": ""})
        assert response._get("value") == ""

    def test_field_is_zero(self):
        """_get should return 0 (not NA) when value is zero."""
        response = BaseResponse(_raw_data={"value": 0})
        assert response._get("value") == 0

    def test_field_is_false(self):
        """_get should return False (not NA) when value is False."""
        response = BaseResponse(_raw_data={"value": False})
        assert response._get("value") is False


class TestBaseResponseNASentinel:
    """Tests for NA sentinel behavior."""

    def test_na_is_singleton(self):
        """NA sentinel should be a singleton for identity comparison."""
        response1 = BaseResponse(_raw_data={})
        response2 = BaseResponse(_raw_data={})
        assert response1._get("missing") is response2._get("missing")
        assert response1._get("missing") is NA

    def test_na_vs_none_distinction(self):
        """NA and None should be distinguishable for absent vs null fields."""
        response = BaseResponse(_raw_data={"explicit_null": None})
        assert response._get("explicit_null") is None
        assert response._get("absent_field") is NA
        assert response._get("explicit_null") is not NA
        assert response._get("absent_field") is not None


class TestBaseResponseNew:
    """Tests for _new method - creating single nested objects."""

    def test_field_with_data(self):
        """_new should create nested object when field has JSON data."""
        user = User(
            _raw_data={
                "name": "Alice",
                "contact": {"phone": "123-456", "email": "alice@example.com"},
            }
        )
        contact = user.contact
        assert isinstance(contact, Contact)
        assert contact.phone == "123-456"
        assert contact.email == "alice@example.com"

    def test_field_is_none(self):
        """_new should return None when field value is explicitly None."""
        user = User(_raw_data={"name": "Alice", "contact": None})
        assert user.contact is None

    def test_field_absent(self):
        """_new should return NA sentinel when field is absent."""
        user = User(_raw_data={"name": "Alice"})
        assert user.contact is NA

    def test_nested_access_after_new(self):
        """Nested object should provide access to its own raw_data."""
        contact_data = {"phone": "123-456", "email": "test@test.com"}
        user = User(_raw_data={"contact": contact_data})
        contact = user.contact
        assert contact.raw_data == contact_data


class TestBaseResponseNewMany:
    """Tests for _new_many method - creating lists of nested objects."""

    def test_field_with_list(self):
        """_new_many should create list of objects when field has array data."""
        user = User(
            _raw_data={
                "name": "Alice",
                "addresses": [
                    {"city": "New York", "zip_code": "10001"},
                    {"city": "Boston", "zip_code": "02101"},
                ],
            }
        )
        addresses = user.addresses
        assert isinstance(addresses, list)
        assert len(addresses) == 2
        assert all(isinstance(addr, Address) for addr in addresses)
        assert addresses[0].city == "New York"
        assert addresses[0].zip_code == "10001"
        assert addresses[1].city == "Boston"
        assert addresses[1].zip_code == "02101"

    def test_field_with_empty_list(self):
        """_new_many should return empty list when field has empty array."""
        user = User(_raw_data={"addresses": []})
        addresses = user.addresses
        assert isinstance(addresses, list)
        assert len(addresses) == 0

    def test_field_is_none(self):
        """_new_many should return None when field value is explicitly None."""
        user = User(_raw_data={"addresses": None})
        assert user.addresses is None

    def test_field_absent(self):
        """_new_many should return NA sentinel when field is absent."""
        user = User(_raw_data={"name": "Alice"})
        assert user.addresses is NA

    def test_single_item_list(self):
        """_new_many should work correctly with single-item arrays."""
        user = User(_raw_data={"addresses": [{"city": "Chicago", "zip_code": "60601"}]})
        addresses = user.addresses
        assert len(addresses) == 1
        assert addresses[0].city == "Chicago"


class TestBaseResponseImmutability:
    """Tests for frozen dataclass behavior."""

    def test_cannot_modify_raw_data_attribute(self):
        """BaseResponse should be immutable (frozen dataclass)."""
        response = BaseResponse(_raw_data={"key": "value"})
        with pytest.raises(dataclasses.FrozenInstanceError):
            response._raw_data = {}


if __name__ == "__main__":
    from sanhe_confluence_sdk.tests import run_cov_test

    run_cov_test(
        __file__,
        "sanhe_confluence_sdk.methods.model",
        preview=False,
    )
