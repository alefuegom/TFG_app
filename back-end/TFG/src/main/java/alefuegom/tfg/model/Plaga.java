package alefuegom.tfg.model;

import javax.persistence.Entity;
import javax.persistence.Table;
import javax.validation.constraints.NotBlank;

@Entity
@Table(name="plagas")
public class Plaga extends BaseEntity{
	
	@NotBlank
	private String nombre;

}
