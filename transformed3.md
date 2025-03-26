# Splunk to OpenSearch Query Transformation

## Complex Ticket Duration Query

### Original Splunk Query:
```
sourcetype="complex_query"   
| eval ticket_end_time = if(actionCode=="D",strptime(actionTime,"%Y/%m/%d %H:%M:%S"),NULL)   
| eval ticket_start_time = if(actionCode=="I",strptime(firstOccurrence,"%Y/%m/%d %H:%M:%S"),NULL)   
| transaction serverName serverSerial ticketNumber   
| eval ticketDuration = ticket_end_time - ticket_start_time   
| eval pretty_ticketDuration = floor(ticketDuration/60/60)." Hours ".floor(floor(ticketDuration - (floor(ticketDuration/60/60)*60*60))/60)." Min ".floor(ticketDuration%60)." Sec."   
| stats avg(ticketDuration) AS Average_Ticket_Duration list(pretty_ticketDuration) AS pretty_ticketDuration by serverName serverSerial
```

### OpenSearch Equivalent:

```
GET /index_name/_search
{
  "size": 0,
  "query": {
    "term": {
      "sourcetype.keyword": "complex_query"
    }
  },
  "aggs": {
    "by_serverName": {
      "terms": {
        "field": "serverName.keyword",
        "size": 1000
      },
      "aggs": {
        "by_serverSerial": {
          "terms": {
            "field": "serverSerial.keyword",
            "size": 1000
          },
          "aggs": {
            "by_ticketNumber": {
              "terms": {
                "field": "ticketNumber.keyword",
                "size": 10000
              },
              "aggs": {
                "ticket_details": {
                  "scripted_metric": {
                    "init_script": "state.tickets = [:]",
                    "map_script": """
                      String serverName = doc['serverName.keyword'].value;
                      String serverSerial = doc['serverSerial.keyword'].value;
                      String ticketNumber = doc['ticketNumber.keyword'].value;
                      String key = serverName + '|' + serverSerial + '|' + ticketNumber;
                      
                      if (state.tickets[key] == null) {
                        state.tickets[key] = [:]
                      }
                      
                      if (doc['actionCode.keyword'].value == 'D') {
                        ZonedDateTime actionTime = doc['actionTime'].value;
                        if (actionTime != null) {
                          state.tickets[key].end_time = actionTime.toInstant().toEpochMilli() / 1000;
                        }
                      } else if (doc['actionCode.keyword'].value == 'I') {
                        ZonedDateTime firstOccurrence = doc['firstOccurrence'].value;
                        if (firstOccurrence != null) {
                          state.tickets[key].start_time = firstOccurrence.toInstant().toEpochMilli() / 1000;
                        }
                      }
                    """,
                    "combine_script": "return state.tickets",
                    "reduce_script": """
                      Map result = new HashMap();
                      result.durations = [];
                      result.pretty_durations = [];
                      
                      for (state in states) {
                        if (state == null) continue;
                        
                        for (entry in state.entrySet()) {
                          Map ticket = entry.getValue();
                          if (ticket.containsKey('start_time') && ticket.containsKey('end_time')) {
                            long duration = ticket.end_time - ticket.start_time;
                            result.durations.add(duration);
                            
                            // Calculate pretty duration
                            int hours = (int) Math.floor(duration / 60 / 60);
                            int mins = (int) Math.floor((duration - (hours * 60 * 60)) / 60);
                            int secs = (int) (duration % 60);
                            String prettyDuration = hours + " Hours " + mins + " Min " + secs + " Sec.";
                            result.pretty_durations.add(prettyDuration);
                          }
                        }
                      }
                      
                      // Calculate average
                      if (!result.durations.isEmpty()) {
                        double sum = 0;
                        for (duration in result.durations) {
                          sum += duration;
                        }
                        result.avg_duration = sum / result.durations.size();
                      } else {
                        result.avg_duration = 0;
                      }
                      
                      return result;
                    """
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
```

### Alternative Approach Using Two Queries:

Since OpenSearch doesn't have a native "transaction" command like Splunk, you could also implement this as two separate queries and process the results in your application code:

#### Step 1: Get all ticket start events
```
GET /index_name/_search
{
  "size": 10000,
  "query": {
    "bool": {
      "must": [
        { "term": { "sourcetype.keyword": "complex_query" } },
        { "term": { "actionCode.keyword": "I" } }
      ]
    }
  },
  "_source": ["serverName", "serverSerial", "ticketNumber", "firstOccurrence"]
}
```

#### Step 2: Get all ticket end events
```
GET /index_name/_search
{
  "size": 10000,
  "query": {
    "bool": {
      "must": [
        { "term": { "sourcetype.keyword": "complex_query" } },
        { "term": { "actionCode.keyword": "D" } }
      ]
    }
  },
  "_source": ["serverName", "serverSerial", "ticketNumber", "actionTime"]
}
```

Then in your application code, you would:
1. Match the start and end events by serverName, serverSerial, and ticketNumber
2. Calculate the duration for each ticket
3. Compute the average duration and format the pretty duration for each group

## Notes on this Transformation:

1. The OpenSearch equivalent uses a scripted metric aggregation to simulate Splunk's transaction processing - this requires script permissions to be enabled.

2. The main challenges in this transformation are:
   - OpenSearch doesn't have direct equivalents for Splunk's eval functions
   - The transaction command in Splunk needs to be simulated in OpenSearch
   - Date parsing and calculation need to be handled differently

3. Performance considerations:
   - For large datasets, the scripted metric approach might be resource-intensive
   - Consider using the two-query approach and process the data in your application code

4. The transformation assumes date fields (actionTime and firstOccurrence) are properly mapped as date types in OpenSearch. If they're stored as strings, additional parsing would be required.

5. You may need to adjust the field names to match your actual OpenSearch index mappings.