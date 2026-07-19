from datetime import timezone

import pytest

from core.event_model import CommonEvent
from parsers.evtx_parser import _event_from_xml, parse


SAMPLE_EVTX_XML = """<?xml version="1.0" encoding="utf-8"?>
<Event xmlns="http://schemas.microsoft.com/win/2004/08/events/event">
  <System>
    <Provider Name="Application Error" Guid="{00000000-0000-0000-0000-000000000000}" />
    <EventID Qualifiers="0">1000</EventID>
    <Version>0</Version>
    <Level>2</Level>
    <Task>100</Task>
    <Opcode>0</Opcode>
    <Keywords>0x80000000000000</Keywords>
    <TimeCreated SystemTime="2024-01-10T09:00:00.000000Z" />
    <EventRecordID>42</EventRecordID>
    <Correlation ActivityID="{11111111-1111-1111-1111-111111111111}" />
    <Execution ProcessID="1234" ThreadID="5678" />
    <Channel>Application</Channel>
    <Computer>WINLAB01</Computer>
    <Security UserID="S-1-5-18" />
  </System>
  <EventData>
    <Data Name="AppName">demo.exe</Data>
    <Data Name="ExceptionCode">0xc0000005</Data>
  </EventData>
</Event>
"""


SECOND_EVTX_XML = """<?xml version="1.0" encoding="utf-8"?>
<Event xmlns="http://schemas.microsoft.com/win/2004/08/events/event">
  <System>
    <Provider Name="Service Control Manager" />
    <EventID>7036</EventID>
    <TimeCreated SystemTime="2024-01-10T09:05:00Z" />
    <EventRecordID>43</EventRecordID>
    <Channel>System</Channel>
    <Computer>WINLAB01</Computer>
  </System>
  <EventData>
    <Data Name="param1">Windows Event Log</Data>
    <Data Name="param2">running</Data>
  </EventData>
  <UserData>
    <ServiceStatus>
      <ServiceName>EventLog</ServiceName>
      <State>running</State>
    </ServiceStatus>
  </UserData>
</Event>
"""


MISSING_TIMESTAMP_XML = """<?xml version="1.0" encoding="utf-8"?>
<Event xmlns="http://schemas.microsoft.com/win/2004/08/events/event">
  <System>
    <Provider Name="Application Error" />
    <EventID>1000</EventID>
    <Channel>Application</Channel>
  </System>
</Event>
"""


def test_event_from_xml_generates_common_event(tmp_path):
    event = _event_from_xml(SAMPLE_EVTX_XML, tmp_path / "Application.evtx", record_number=7)

    assert isinstance(event, CommonEvent)
    assert event.source_artifact == "EVTX"
    assert event.event_category == "system_event"
    assert event.event_action == "windows_event"


def test_event_from_xml_timestamp_is_timezone_aware_utc(tmp_path):
    event = _event_from_xml(SAMPLE_EVTX_XML, tmp_path / "Application.evtx", record_number=7)

    assert event is not None
    assert event.timestamp_utc.tzinfo is not None
    assert event.timestamp_utc.utcoffset() is not None
    assert event.timestamp_utc.tzinfo == timezone.utc


def test_event_from_xml_object_contains_channel_and_event_id(tmp_path):
    event = _event_from_xml(SAMPLE_EVTX_XML, tmp_path / "Application.evtx", record_number=7)

    assert event is not None
    assert event.object == "Application:1000"


def test_event_from_xml_raw_evidence_contains_expected_fields(tmp_path):
    event = _event_from_xml(SAMPLE_EVTX_XML, tmp_path / "Application.evtx", record_number=7)

    assert event is not None
    assert event.raw_evidence["provider_name"] == "Application Error"
    assert event.raw_evidence["event_id"] == "1000"
    assert event.raw_evidence["channel"] == "Application"
    assert event.raw_evidence["event_record_id"] == "42"
    assert event.raw_evidence["event_data"]["AppName"] == "demo.exe"


def test_event_from_xml_provenance_contains_timestamp_details(tmp_path):
    event = _event_from_xml(SAMPLE_EVTX_XML, tmp_path / "Application.evtx", record_number=7)

    assert event is not None
    assert event.provenance["original_timestamp"] == "2024-01-10T09:00:00.000000Z"
    assert event.provenance["normalization_method"] == "parse_iso_to_utc"
    assert event.provenance["timestamp_field"] == "System.TimeCreated.SystemTime"


def test_event_from_xml_extracts_simple_user_data(tmp_path):
    event = _event_from_xml(SECOND_EVTX_XML, tmp_path / "System.evtx", record_number=8)

    assert event is not None
    assert event.object == "System:7036"
    assert event.raw_evidence["user_data"]["ServiceStatus"]["ServiceName"] == "EventLog"


def test_event_from_xml_without_time_created_returns_none(tmp_path):
    with pytest.warns(RuntimeWarning, match="missing System/TimeCreated"):
        event = _event_from_xml(MISSING_TIMESTAMP_XML, tmp_path / "Application.evtx")

    assert event is None


def test_parse_empty_folder_returns_empty_list(tmp_path):
    assert parse(tmp_path) == []


def test_parse_non_evtx_file_returns_empty_list(tmp_path):
    text_file = tmp_path / "not-an-evtx.txt"
    text_file.write_text("not evtx", encoding="utf-8")

    assert parse(text_file) == []


def test_parse_corrupt_evtx_file_does_not_break(tmp_path):
    corrupt_file = tmp_path / "corrupt.evtx"
    corrupt_file.write_text("not a valid evtx file", encoding="utf-8")

    with pytest.warns(RuntimeWarning):
        events = parse(tmp_path)

    assert events == []
