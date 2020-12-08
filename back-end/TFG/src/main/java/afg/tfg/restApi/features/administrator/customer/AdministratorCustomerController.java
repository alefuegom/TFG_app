package afg.tfg.restApi.features.administrator.customer;

import java.util.Collection;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import afg.tfg.restApi.model.Customer;

@RestController
@CrossOrigin(origins="http://localhost:4200")
public class AdministratorCustomerController {
	
	@Autowired
	private AdministratorCustomerRepository repository;
	
	@GetMapping(value="administrator/customers")
	public Collection<Customer> findAllCustomers(){
		return (Collection<Customer>) repository.findAll();	
	}
	
	

}
